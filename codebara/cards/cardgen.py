"""from threading import Thread"""

import base64
import datetime
import http.client
import json
import math
from pathlib import Path
from io import BytesIO
from threading import Thread
from typing import Final
import os
from aiohttp import web
from PIL import Image
from codebara.tools.common import splitmix64, build_seed
from codebara.cards.cardMysql import register_requestCard
from codebara.cards.imageCardCreator import CardImageCreator, CardSpecs, SpecialSpec
from codebara.config import (
    IMAGE_IA_GEN_BODY_BASE,
    IMAGE_IA_GEN_ENDPOINT_GEN,
    IMAGE_IA_GEN_ENDPOINT_METHOD,
    IMAGE_IA_GEN_REST_URL,
)
from codebara.seasons.season import seasonLoader
from codebara.tools.common import seededRandom
from codebara.users import user

# from codebara.errors import HttpOutputResponse
DEBUG_USERCORE_DATAS = user.UserCoreDatas(-1, 12)
MIN_WEIGHT: Final[float] = 1e-9

class CardGenerator:
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
    seasons:list[dict]
    centralImageId: str
    specs: CardSpecs
    specialSpecs: list[SpecialSpec]

    def __init__(
        self,
        #season: dict | None = None,
        seasons:list[dict],
        userDatas: user.UserCoreDatas = DEBUG_USERCORE_DATAS,
    ):
        print("generator instanciate for user:" + str(userDatas.uid))
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
            seasonSeed=self.season["seasonSeed"]
        except AttributeError:
            seasonSeed=2543254
        seed = build_seed(seed_user=self.userDatas.seed,season_seed= seasonSeed,cb_field_input= cb_field_input
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

        seed = build_seed(self.userDatas.seed,self.season['seasonSeed'], cbfield)

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

    async def generate(self, cb: str):
        self.realcb = cb
        self.cb = cb
        self._barcodeStandardization(self.promptUserSeed)
        self._calculate()
        self.temporaryId = await self._registerRequest()
        self._checkIfImageAlredyExist()
        if not self.isNewImage:
            self._createImage()
        else:
            self._assembleRequest()
            # renderPool.push(self._syncCreateCard)
            t = Thread(target=self._syncCreateCard)
            t.start()
        return self.temporaryId

    def _createImage(self):
        print("create image")
        creator = CardImageCreator(self.userDatas.uid, self.season)
        loc = creator.create(self.specs, '.'+self.season['ressourcesFolder']+'/'+self.centralImageId+".png")
        print("output:" + loc)

    def _calculate(self):
        #calcul de la saison
        self.season=self.seasons[self._deterministic_weighted_choice(self.seasons,int(self.cb))]
        # creation du prompt
        self.prompt = self.season["promptBase"]
        imageId=""
        for part in self.season["barcodeData"]["prompt"]:
            print(part["name"])
            cbValueForPart = int(self.cb[part["bitposition"]: -(len(self.cb)-part["bitposition"]-part["bitsize"])])
            valueindex = self._deterministic_weighted_choice(
                part["values"], cbValueForPart
            )
            imageId+=str(valueindex)
            self.prompt += ";" + part["values"][valueindex]["value"]
            self.selectedContent.append(part["values"][valueindex])
        # end for
        self.centralImageId = str(self.season['seasonid'])+"_" + imageId+'_'+str(self.userDatas.seed)
        #calculate basics values
        part=self.season["barcodeData"]['health']
        cbValueForPart = int(self.cb[part["bitposition"]: -(len(self.cb)-part["bitposition"]-part["bitsize"])])
        health=self._deterministic_weighted_value(part["min"],part["max"],part["factor"],cbValueForPart)
        part=self.season["barcodeData"]['attack']
        cbValueForPart = int(self.cb[part["bitposition"]: -(len(self.cb)-part["bitposition"]-part["bitsize"])])
        attack=self._deterministic_weighted_value(part["min"],part["max"],part["factor"],cbValueForPart)
        self.specs=CardSpecs(name="",attack=attack,health=health,specs=None)

        print("calculatedCard")
        print(self)

    def _syncCreateCard(self):
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
            print(jsonObj["images"][0])
            conn.close()
            if os.path.isdir('.'+self.season['ressourcesFolder']) is not True:
                os.makedirs('.'+self.season['ressourcesFolder'])
            with open('.'+self.season['ressourcesFolder']+'/'+self.centralImageId+".json", "w") as fout:
                json.dump(jsonObj, fout)
            file_content = jsonObj["images"][0]
            image_bytes = base64.b64decode(file_content)
            image = Image.open(BytesIO(image_bytes))
            image.save("." + self.season['ressourcesFolder']+'/'+self.centralImageId+".png", format="PNG")
            self._createImage()
        except KeyError:
            print("error http")
        print("request IA")

    async def _registerRequest(self):
        print("get temporaryId")
        self.temporaryId = await register_requestCard(
            userid=self.userDatas.uid, request=self.IArequest
        )
        return self.temporaryId

    def _assembleRequest(self):
       # construction de la requete IA a partir de la base de requete
        self.IArequest["prompt"] = self.prompt
        print(json.dumps(self.IArequest))
        self.IArequest["seed"] = self.userDatas.seed

    def _checkIfImageAlredyExist(self):
        my_file = Path('.'+self.season['ressourcesFolder']+'/'+self.centralImageId+".png")
        if my_file.is_file():
            return True
        else:
            return False

    def _finalizeCardOndb(self):
        print("set on db finalization of card")


    def toResponse(self, request) -> web.Response:
        print("to web response")
        return (
            web.Response()
        )  # HttpOutputResponse(error=HttpErrors.OK, request=request).toResponse()con
