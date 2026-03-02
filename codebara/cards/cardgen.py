from threading import Thread
import datetime
from aiohttp import web
import math
import random
#from codebara.errors import HttpOutputResponse
class CardGenerator:
    uid:int
    realcb:str
    cb:str
    dateRequest:datetime.datetime
    prompt:str=''
    isNewImage:bool=True
    temporaryId:int|None
    imageId:int=-1
    estimatedTime:int=60
    seed:int
    
    def __init__(self,cb:str,uid:int=1):
        print('generator instanciate for '+str(uid))
        self.uid=uid
        self.realcb=cb
        self.cb=cb
        self._getSeed()
        self.barcodeStandardization(self.seed)
        CardGenerator.seededRandom(self.seed, self.seed)
        self.dateRequest=datetime.datetime.now()
    def barcodeStandardization(self,seed:int,finalSize=128):
        counter = math.floor(finalSize / len(self.cb))
        finalCode=""
        index=0
        while index < counter:
        #for index in counter:
            finalCode += self.cb
            index+=1
        toAdd = finalSize - len(finalCode)
        prng = CardGenerator.seededRandom(self.seed, int(self.cb))
        position = math.floor(prng * 10) % len(finalCode) - toAdd
        finalCode += finalCode[position: position + toAdd] 
        self.cb=finalCode  
    @staticmethod
    def seededRandom(   seed1: int,seed2:int,
                        min: int = 1,max: int = 100000,
                        renderProb = 0.5) :
        c = 2147483647 # Un grand nombre premier

        seed = (1664525 * (seed1 ^ seed2) + 1013904223) % c 
        seed = (seed * 48271) % c #Applique un multiplicateur supplémentaire pour plus d'aléatoire

        # Génère un nombre pseudo-aléatoire entre 0 et 1 basé sur la graine
        probabilityFactor = (seed % 10000) / 10000

        #Génération d'un ajustement probabiliste reproductible
        biasSeed = (seed * 16807) % c # Applique un autre calcul basé sur le seed
        biasFactor =(biasSeed % 10000) / 10000 < probabilityFactor if renderProb>0.5 else (1 - probabilityFactor)

        return math.floor(min + biasFactor * (max - min)) # Assure que la valeur est entre min et max
  
    def generate(self):
        self._registerCreation()
        self._calculate()
        self._checkIfImageAlredyExist()
        if not self.isNewImage:
            self._createImage()
        else:
            self._assembleRequest()
            Thread(target=self._syncCreateCard)
        return self
    def _createImage(self):
        print("create image")
    def _calculate(self):
        print("calculateCard")
    def _syncCreateCard(self):
        print("request IA")
    def _registerCreation(self):
        print('get temporaryId')
    def _getPrompt(self):
        print('create Prompt')
    def _assembleRequest(self):
        #self._assembleRequest()
        print('assemble request')
    def _checkIfImageAlredyExist(self):
        print("check if image already generated")
    def _finalizeCardOndb(self):
        print("set on db finalization of card")
    def _getSeed(self):
        self.seed=random.randint(2,1000)
        print("get user Seed")
    def toResponse(self,request)->web.Response:
        print("to web response")
        return web.Response()#HttpOutputResponse(error=HttpErrors.OK, request=request).toResponse()