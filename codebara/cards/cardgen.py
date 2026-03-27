import base64
import datetime
import http.client
import json
import math
import os
import asyncio
from io import BytesIO
from pathlib import Path
import shutil
from threading import Thread
from typing import Final
import tarfile
import hashlib
from aiohttp import web
from PIL import Image
from codebara.cards.cardMysql import register_requestCard, update_registered_requestCard, checkCardOwner
from codebara.cards.imageCardCreator import CardImageCreator, CardSpecs, SpecialSpec
from codebara.config import (
    IMAGE_IA_GEN_BODY_BASE,
    IMAGE_IA_GEN_ENDPOINT_GEN,
    IMAGE_IA_GEN_ENDPOINT_METHOD,
    IMAGE_IA_GEN_REST_URL,
    OUTPUT_CARD_SIZE,
    CARD_FILE_EXTENSION
)
#from codebara.seasons.season import seasonLoader
from codebara.tools.common import build_seed, seededRandom, splitmix64
from codebara.tools import getSha256FromFile
from codebara.users import user
TEST = True
# from codebara.errors import HttpOutputResponse
h = hashlib.new('sha256')
h.update(b"godmdp")
DEBUG_USERCORE_DATAS = user.UserCoreDatas(-1, 12,h.hexdigest())
MIN_WEIGHT: Final[float] = 1e-9


class CardGenerator:
    cardId:int
    userDatas: user.UserCoreDatas
    realcb: str
    cb: str
    dateRequest: datetime.datetime
    IArequest: dict
    selectedContent: list[dict] = []
    prompt: str = ""
    isNewImage: bool = True
    temporaryId: int | None
    imageId: int = -1
    estimatedTime: int = 120
    promptUserSeed: int
    season: dict
    seasons: list[dict]
    centralImageId: str
    specs: CardSpecs
    specialSpecs: list[SpecialSpec]

    def __init__(
        self,
        # season: dict | None = None,
        seasons: list[dict],
        userDatas: user.UserCoreDatas = DEBUG_USERCORE_DATAS,
    ):
        print(
            "generator instanciate for user:"
            + str(userDatas.uid)
            + " for seed:"
            + str(userDatas.seed)
        )
        self.userDatas = userDatas
        self.promptUserSeed = userDatas.seed
        seededRandom(self.promptUserSeed, self.promptUserSeed)
        self.dateRequest = datetime.datetime.now()
        """if season is None:
            self.season = seasonLoader()
        else:
            self.season = season"""
        self.seasons = seasons
        self.IArequest = IMAGE_IA_GEN_BODY_BASE

    # https://chatgpt.com/share/69abbae3-ee8c-800a-bd2e-2a3c96223f20

    def _deterministic_weighted_choice(
        self,
        elements: list[dict],
        cb_field_input: int,
    ) -> int:
        """
        Sélection pseudo-aléatoire déterministe pondérée par 'factor'.

        elements : list[dict]
            dict contenant :
            - value
            - factor ∈ [0,1]

        Retourne toujours un indice valide du tableau.
        """

        if not elements:
            raise ValueError("elements ne peut pas être vide")
        try:
            seasonSeed = self.season["seasonSeed"]
        except AttributeError:
            seasonSeed = 2543254
        seed = build_seed(
            seed_user=self.userDatas.seed,
            season_seed=seasonSeed,
            cb_field_input=cb_field_input,
        )

        rand64 = splitmix64(seed)
        r = rand64 / 2**64

        weights = []
        max_factor = -1.0
        least_rare_index = 0

        for i, el in enumerate(elements):

            factor = float(el.get("factor", 0.0))

            if not math.isfinite(factor):
                raise ValueError(f"factor invalide à l'index {i}")

            factor = min(1.0, max(0.0, factor))

            weight = MIN_WEIGHT + factor
            weights.append(weight)

            # on garde l'élément le moins rare (factor le plus proche de 1)
            if factor > max_factor:
                max_factor = factor
                least_rare_index = i

        total_weight = math.fsum(weights)

        target = r * total_weight
        cumulative = 0.0

        for i, w in enumerate(weights):
            cumulative += w
            if cumulative >= target:
                return i

        # fallback sécurité : élément le moins rare de la liste
        return least_rare_index

    def _deterministic_weighted_value(
        self,
        minValue: int,
        maxValue: int,
        factor: float,
        cbfield: int,
    ) -> int:

        if maxValue < minValue:
            raise ValueError("maxValue doit être >= minValue")

        if not math.isfinite(factor):
            factor = 0.0

        factor = min(1.0, max(0.0, factor))

        seed = build_seed(self.userDatas.seed, self.season["seasonSeed"], cbfield)

        rand64 = splitmix64(seed)

        r = rand64 / 2**64

        span = maxValue - minValue

        if span == 0:
            return minValue

        exponent = 1.0 / (0.01 + factor)

        biased = r**exponent

        value = minValue + int(biased * (span + 1))

        if value > maxValue:
            value = maxValue

        if value < minValue:
            value = minValue

        return value

    def _barcodeStandardization(self, seed: int, finalSize=128):
        counter = math.floor(finalSize / len(self.cb))
        finalCode = ""
        index = 0
        while index < counter:
            # for index in counter:
            finalCode += self.cb
            index += 1
        toAdd = finalSize - len(finalCode)
        prng = seededRandom(self.promptUserSeed, int(float(self.cb)))
        position = math.floor(prng * 10) % len(finalCode) - toAdd
        finalCode += finalCode[position : position + toAdd]
        self.cb = finalCode

    async def generate(self, cb: str)->int:
        print("ean13:" + cb)
        self.realcb = cb
        self.cb = cb
        self._barcodeStandardization(self.promptUserSeed)
        self._calculate()
        self._assembleRequest()
        self.temporaryId = await self._registerRequest()
        self.specs.id=self.temporaryId
        self.cardId=self.temporaryId
        self._checkIfImageAlredyExist()
        if not self.isNewImage:
            await self._createImage()
        else:
            # renderPool.push(self._syncCreateCard)
            if TEST is False:
                t = Thread(target=self._asyncCreateCard)
                t.start()
            else:
                await self._syncCreateCard()
        return self.temporaryId
    def _asyncCreateCard(self):
        asyncio.run( self._syncCreateCard())
    async def _createImage(self):
        print("create image")
        creator = CardImageCreator(self.userDatas.uid, self.season)
        loc = creator.create(
            self.specs,
            "." + self.season["ressourcesFolder"] + "/" + self.centralImageId + ".png",
        )
        zipfilename=self.userDatas.serverDataLoc+'/'+str(self.cardId)
        folder=zipfilename
        zipfilename+=CARD_FILE_EXTENSION#".tar.gz"
        p=Path(folder)
        if not p.is_dir():
            p.mkdir(parents=True)
        shutil.move(loc,folder+'/front.png')
        img=Image.open(folder+'/front.png')
        #img=img.resize((int(img.width/1.2),int(img.height/1.2)))
        img.thumbnail(OUTPUT_CARD_SIZE)
        img.save(folder+'/front.png', optimize=True)
        hash={"front":getSha256FromFile(folder+'/front.png')}
        shutil.copyfile("." + self.season["ressourcesFolder"] + "/" + self.centralImageId + ".png", folder+'/perso.png')
        img=Image.open(folder+'/perso.png')
        img.thumbnail((256,256))
        img.save(folder+'/perso.png', optimize=True)
        hash["perso"]=getSha256FromFile(folder+'/perso.png')
        with open(folder+"/datas.json","w") as fout:
            json.dump(self.specs.todict(), fout)
        hash["datas"]=getSha256FromFile(folder+"/datas.json")
        img=Image.open("." + self.season["deck"]['backUrl'])
        #img=img.resize((int(img.width/1.2),int(img.height/1.2)))
        img.thumbnail(OUTPUT_CARD_SIZE)
        img.save(folder+'/back.png', optimize=True)
        hash["back"]=getSha256FromFile(folder+"/back.png")
        cardZone=json.loads(json.dumps(self.season['deck']))
        cardZone['frontUrl']='front.png'
        cardZone['backUrl']='back.png'
        cardZone['persoUrl']='perso.png'
        xratio=cardZone['width']/OUTPUT_CARD_SIZE[0]
        yratio=cardZone['height']/OUTPUT_CARD_SIZE[1]
        cardZone['width']=OUTPUT_CARD_SIZE[0]
        cardZone['height']=OUTPUT_CARD_SIZE[1]
        for key, value in cardZone['positions'].items():
            value['x']=int(value['x']/xratio)+1
            value['y']=int(value['y']/yratio)+1
            if value.get('width'):
                value['width']=int(value['width']/xratio)+1
            if value.get('height'):
                value['height']=int(value['height']/yratio)+1
            print (key, value)
        with open(folder+"/deck.json","w") as fout:
            json.dump(cardZone, fout)
        with open(folder+"/hashs.json","w") as fout:
            json.dump(hash, fout)
        with tarfile.open( zipfilename, "w:xz") as tar:
            for name in os.listdir( folder ):
                #if not name.endswith('card.tar.gz'):
                tar.add(folder+'/'+name, arcname=name)
                os.remove(folder+'/'+name)
        tar.close()
        os.rmdir(folder)
        await update_registered_requestCard(specs=self.specs, cardid=self.cardId, hash=getSha256FromFile(zipfilename),fileloc=zipfilename)


    def _calculate(self):
        # calcul de la saison
        self.season = self.seasons[
            self._deterministic_weighted_choice(self.seasons, int(self.cb))
        ]
        # creation du prompt
        self.prompt = self.season["promptBase"]
        imageId = ""
        for part in self.season["barcodeData"]["prompt"]:
            print(part["name"])
            cbValueForPart = int(
                self.cb[
                    part["bitposition"] : -(
                        len(self.cb) - part["bitposition"] - part["bitsize"]
                    )
                ]
            )
            valueindex = self._deterministic_weighted_choice(
                part["values"], cbValueForPart
            )
            imageId += str(valueindex)
            self.prompt += ";" + part["values"][valueindex]["value"]
            self.selectedContent.append(part["values"][valueindex])
            print(self.prompt)
        # end for
        self.centralImageId = (
            str(self.season["seasonid"])
            + "_"
            + imageId
            + "_"
            + str(self.userDatas.seed)
        )
        # calculate basics values
        part = self.season["barcodeData"]["health"]
        cbValueForPart = int(
            self.cb[
                part["bitposition"] : -(
                    len(self.cb) - part["bitposition"] - part["bitsize"]
                )
            ]
        )
        health = self._deterministic_weighted_value(
            part["min"], part["max"], part["factor"], cbValueForPart
        )
        part = self.season["barcodeData"]["attack"]
        cbValueForPart = int(
            self.cb[
                part["bitposition"] : -(
                    len(self.cb) - part["bitposition"] - part["bitsize"]
                )
            ]
        )
        attack = self._deterministic_weighted_value(
            part["min"], part["max"], part["factor"], cbValueForPart
        )
        #calcul des specials specs
        specials=[]
        seasonSpecials=self.season["barcodeData"]["specials"]
        for bitp in seasonSpecials["bitpositions"]:


            cbValueForPart = int(
                self.cb[
                    bitp : -(
                        len(self.cb) - bitp - seasonSpecials["bitsize"]
                    )
                ]
            )
            valueindex = self._deterministic_weighted_choice(
                seasonSpecials["values"], cbValueForPart
            )
            special=seasonSpecials["values"][valueindex]
            if special.get('name') is not None:
                sattack:int|None=attack+special.get('attack') if special.get('attack') is not None else None
                shealth:int|None=special.get('health') if special.get('health') is not None else None
                if special['type']=="attack" :
                    if sattack is None:
                        cbValueForPart = int(
                            self.cb[
                                special["bitposition"] : -(
                                    len(self.cb) - special["bitposition"] - special["bitsize"]
                                )
                            ]
                        )
                        sattack =attack+ self._deterministic_weighted_value(
                            special["min"], special["max"], special["factorValue"], cbValueForPart
                        )
                elif special['type']=='health':
                    if shealth is None:
                        cbValueForPart = int(
                            self.cb[
                                special["bitposition"] : -(
                                    len(self.cb) - special["bitposition"] - special["bitsize"]
                                )
                            ]
                        )
                        shealth = self._deterministic_weighted_value(
                            special["min"], special["max"], special["factorValue"], cbValueForPart
                        )
                else:
                    if shealth is None:
                        cbValueForPart = int(
                            self.cb[
                                special["bitpositions"][0] : -(
                                len(self.cb) - special["bitpositions"][0] - special["bitsizes"][0]
                                )
                            ]
                        )
                        shealth = self._deterministic_weighted_value(
                            special["mins"][0], special["maxs"][0], special["factorValues"][0], cbValueForPart
                        )
                    if sattack is None:
                        cbValueForPart = int(
                            self.cb[
                                special["bitpositions"][1] : -(
                                len(self.cb) - special["bitpositions"][1] - special["bitsizes"][1]
                                )
                            ]
                        )
                        sattack =attack+ self._deterministic_weighted_value(
                            special["mins"][1], special["maxs"][1], special["factorValues"][1], cbValueForPart
                        )
                sspec=SpecialSpec(name=special['name'], attack=sattack, health=shealth, turn=special['turn'] )
                specials.append(sspec)
        print(specials)
        if len(specials)==0:
            specials=None
        self.specs = CardSpecs(cid=-1, name="", attack=attack, health=health, specials=specials)

        print("calculatedCard")
        print(self)

    async def _syncCreateCard(self):
        try:
            host = IMAGE_IA_GEN_REST_URL
            conn = http.client.HTTPConnection(host)
            conn.request(
                method=IMAGE_IA_GEN_ENDPOINT_METHOD,
                url=IMAGE_IA_GEN_ENDPOINT_GEN,
                body=json.dumps(self.IArequest),
                headers={"Host": host, "Content-Type": "application/json"},
            )
            response = conn.getresponse()
            print(response.status, response.reason)
            data1 = response.read()
            string = data1.decode("utf-8")
            jsonObj = json.loads(string)
            # print(jsonObj["images"][0])
            conn.close()
            if os.path.isdir("." + self.season["ressourcesFolder"]) is not True:
                os.makedirs("." + self.season["ressourcesFolder"])
            with open(
                "."
                + self.season["ressourcesFolder"]
                + "/"
                + self.centralImageId
                + ".json",
                "w",
            ) as fout:
                json.dump(jsonObj, fout)
            file_content = jsonObj["images"][0]
            image_bytes = base64.b64decode(file_content)
            image = Image.open(BytesIO(image_bytes))
            image.save(
                "."
                + self.season["ressourcesFolder"]
                + "/"
                + self.centralImageId
                + ".png",
                format="PNG",
            )
            await self._createImage()
        except KeyError as e:
            print("error http")
            print(e)
        except ConnectionRefusedError as e:
            print('IA SERVER OFF')
            print(e)
        """except Exception as e:
            print(e)"""
        print("request IA")

    async def _registerRequest(self)->int:
        print("get temporaryId")
        self.temporaryId = await register_requestCard(
            userid=self.userDatas.uid, request=self.IArequest, seasonid=self.season["seasonid"]
        )
        return self.temporaryId

    def _assembleRequest(self):
        # construction de la requete IA a partir de la base de requete
        self.IArequest["prompt"] = self.prompt
        print(json.dumps(self.IArequest))
        self.IArequest["seed"] = self.userDatas.seed

    def _checkIfImageAlredyExist(self):
        my_file = Path(
            "." + self.season["ressourcesFolder"] + "/" + self.centralImageId + ".png"
        )
        if my_file.is_file():
            self.isNewImage = False
            return True
        else:
            self.isNewImage = True
            return False

    def _finalizeCardOndb(self):
        print("set on db finalization of card")

    def toResponse(self, request) -> web.Response:
        print("to web response")
        return (
            web.Response()
        )  # HttpOutputResponse(error=HttpErrors.OK, request=request).toResponse()con
def changeCardNameInFile(file:str,name:str):
    with tarfile.open(file) as cardFile:
        print(cardFile.getnames())
        fileNameSplit=file.split('/')
        repfolder='./tmp/untar/'+fileNameSplit[len(fileNameSplit)-1][:-4]
        if Path(repfolder).exists():
            shutil.rmtree(repfolder)
        Path(repfolder).mkdir(parents=True)
        cardFile.extractall(repfolder)
        cardFile.close()
        datas=None
        with open(repfolder+'/datas.json') as datasJson:
            datas=json.load(datasJson)
            datas['name']=name
            datasJson.close()
        with open(repfolder+'/datas.json',"w") as fout:
            json.dump(datas, fout)
            fout.close()
        with open(repfolder+'/hashs.json') as datasJson:
            datas=json.load(datasJson)
            datas['datas']=getSha256FromFile(repfolder+'/datas.json')
            datasJson.close()
        with open(repfolder+'/hashs.json',"w") as fout:
            json.dump(datas, fout)
        os.remove(file)
        with tarfile.open( file, "w:xz") as tar:
            for name in os.listdir( repfolder ):
                #if not name.endswith('card.tar.gz'):
                tar.add(repfolder+'/'+name, arcname=name)
                os.remove(repfolder+'/'+name)
        shutil.rmtree(repfolder)
        tar.close()
async def setCardName(uid:int,cid:int,name:str)->bool:
    fileloc=await checkCardOwner(uid,cid)
    if fileloc is not None:
        changeCardNameInFile(file=fileloc,name=name)
        await update_registered_requestCard(cardid=cid,name=name, hash=getSha256FromFile(fileloc))
        return True
    else:
        return False