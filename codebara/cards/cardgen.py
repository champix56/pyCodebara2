"""from threading import Thread"""
import base64
import datetime
from aiohttp import web
import math
import random
import json
from codebara.users import user
from codebara.seasons.season import seasonLoader
from codebara.cards.cardMysql import register_requestCard
from codebara.config import IMAGE_IA_GEN_BODY_BASE, IMAGE_IA_GEN_REST_URL, IMAGE_IA_GEN_ENDPOINT_GEN, IMAGE_IA_GEN_ENDPOINT_METHOD
import http.client
from codebara.tools.common import seededRandom
from codebara.cards.imageCardCreator import CardImageCreator, CardSpecs, SpecialSpec
from io import BytesIO
from PIL import Image
#from codebara.ThreadPool.Pool import renderPool
from threading import Thread
#from codebara.errors import HttpOutputResponse
DEBUG_USERCORE_DATAS=user.UserCoreDatas(-1,12)
class CardGenerator:
    userDatas:user.UserCoreDatas
    realcb:str
    cb:str
    dateRequest:datetime.datetime
    IArequest:dict
    selectedContent:list[dict]=[]
    prompt:str=''
    isNewImage:bool=True
    temporaryId:int|None
    imageId:int=-1
    estimatedTime:int=120
    seed:int
    season:dict
    centralImageId:str
    specs:CardSpecs
    specialSpecs:list[SpecialSpec]
    def __init__(self,season:dict|None=None,userDatas:user.UserCoreDatas=DEBUG_USERCORE_DATAS):
        print('generator instanciate for user:'+str(userDatas.uid))
        self.userDatas=userDatas
        self.seed=userDatas.seed
        seededRandom(self.seed, self.seed)
        self.dateRequest=datetime.datetime.now()
        if season is None:
            self.season=seasonLoader()
        else:
            self.season=season
        self.IArequest=IMAGE_IA_GEN_BODY_BASE
    def barcodeStandardization(self,seed:int,finalSize=128):
        counter = math.floor(finalSize / len(self.cb))
        finalCode=""
        index=0
        while index < counter:
        #for index in counter:
            finalCode += self.cb
            index+=1
        toAdd = finalSize - len(finalCode)
        prng = seededRandom(self.seed, int(float(self.cb)))
        position = math.floor(prng * 10) % len(finalCode) - toAdd
        finalCode += finalCode[position: position + toAdd] 
        self.cb=finalCode  
    async def generate(self, cb:str):
        self.realcb=cb
        self.cb=cb
        self.barcodeStandardization(self.seed)
        self._calculate()
        self.temporaryId=await self._registerRequest()
        self._checkIfImageAlredyExist()
        if not self.isNewImage:
            self._createImage()
        else:
            self._assembleRequest()
            #renderPool.push(self._syncCreateCard)
            t=Thread(target=self._syncCreateCard)
            t.start()
        return self.temporaryId
    def _createImage(self):
       print("create image")
    def _calculate(self):
        centralId='_'+str(random.randint(1234,1345678765432))
        self.specialSpecs=[SpecialSpec(name="spacial1", attack=0, health=10)]
        self.specs=CardSpecs("",50,100, self.specialSpecs)
        self.prompt=";panda;avec un rouleau de papier toilette"
        self.centralImageId=centralId

        #creation du prompt
        self.prompt=self.season['promptBase']
        for part in self.season['barcodeData']['prompt']:
            print(part['name'])
            valueindex=random.randint(0,len(part['values'])-1)
            self.prompt+=';'+part['values'][valueindex]['value']
            self.selectedContent.append(part['values'][valueindex])
        # end for

        #construction de la requete IA a partir de la base de requete
        self.IArequest['prompt']=self.prompt
        print(json.dumps(self.IArequest))
        self.IArequest['seed']=self.userDatas.seed
        print("calculatedCard")
        print(self)
    def _syncCreateCard(self):
        try:
            host = IMAGE_IA_GEN_REST_URL
            conn= http.client.HTTPConnection(host)
            self.IArequest['prompt']+=self.prompt
            conn.request(method=IMAGE_IA_GEN_ENDPOINT_METHOD,url= IMAGE_IA_GEN_ENDPOINT_GEN,body=json.dumps(self.IArequest), headers={"Host": host,"Content-Type":"application/json"})
            response = conn.getresponse()
            print(response.status, response.reason)
            data1=response.read()
            string = data1.decode('utf-8')
            jsonObj=json.loads(string)
            print(jsonObj['images'][0])
            conn.close()
            with open('./outputfile', 'w') as fout:
                json.dump(jsonObj, fout)
            file_content =jsonObj['images'][0]
            image_bytes = base64.b64decode(file_content)
            image = Image.open(BytesIO(image_bytes))
            image.save("./"+self.centralImageId+".png", format="PNG")
            creator=CardImageCreator(self.userDatas.uid,self.season)
            loc=creator.create(self.specs,"./"+self.centralImageId+".png" )
            print("output:"+loc)
        except KeyError:
            print("error http")
        print("request IA")
    async def _registerRequest(self):
        print('get temporaryId')
        self.temporaryId=await register_requestCard(userid= self.userDatas.uid,request=self.IArequest)
        return self.temporaryId
    def _getPrompt(self):
        print('create Prompt')
    def _assembleRequest(self):
        #self._assembleRequest()
        print('assemble request')
    def _checkIfImageAlredyExist(self):
        print("check if image already generated")
    def _finalizeCardOndb(self):
        print("set on db finalization of card")
    """def _getSeed(self):
        self.seed=random.randint(2,1000)
        print("get user Seed")"""
    def toResponse(self,request)->web.Response:
        print("to web response")
        return web.Response()#HttpOutputResponse(error=HttpErrors.OK, request=request).toResponse()con