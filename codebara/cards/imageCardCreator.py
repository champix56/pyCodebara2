from PIL import Image, ImageFont,ImageDraw
from codebara.cards.cardgen import CardGenerator
from codebara.cards.card import SpecialSpec, CardSpecs
import json
import random
class CardImageCreator:
    id:int
    specs:CardSpecs
    season:dict
    outCardHeight:int
    outCardWidth:int
    outLoc:str
    tmpImage:Image.Image
    def __init__(self,season:dict|None=None,specs:CardSpecs=None):#outw=2370,outh=4096):
        self.id=int(random.random()*100000*CardGenerator.seededRandom(1000,int(random.random()*1000)))
        if(specs is None):
            self.specs=CardSpecs()
        else:
            self.specs=specs
        if(season is None):
            self.season=self._loadSeason()
        self.outCardWidth=self.season['deck']['width']#outw
        self.outCardHeight=self.season['deck']['width']#outh
        self.outLoc="/"+str(self.id)+".png"
    def _loadSeason(self,location='./season/season.json')->dict:
        with open(location, "r") as jsonfile: 
            data = json.load(jsonfile)
            print(type(data))
            print((data))
            return data
    def create(self,name):
        self._createEmptyBase('./season/standard/front.png')
        self._addPerso(loc='./season/beta/2.png')
        self._addName(name,100,100,200)
        self._addAttack(100)
        self._addHealth(0)
        self._addSpecials()
        self._addSerialNumber(serial=str(self.id), x= 50, y= 3990)
        self.tmpImage.save('.'+self.outLoc)
        print('.'+self.outLoc)
        self.tmpImage.close()
    def _createEmptyBase(self,deckloc:str):
        im = Image.new('RGBA',(self.outCardWidth, self.outCardHeight))
        try:
            with Image.open(deckloc) as im2:
                rgba=im2.convert("RGBA")
                print(deckloc, im.format, f"{im.size}x{im.mode}")
                print(deckloc, im2.format, f"{im2.size}x{im2.mode}")
                im.paste(rgba,(0,0,im2.size[0],im2.size[1]))
        except OSError as e:
            print(e)
        self.tmpImage=im
        return self.outLoc
    def _addPerso(self,loc:str,x:int=108,y:int=367,w:int=2151,h:int=1981):
        i=self.tmpImage
        persoIm=Image.open(loc).convert('RGBA')
        persoImg=persoIm.resize((w,h)).convert('RGBA')
        try:
            i.paste(persoImg,(x,y))
        except ValueError as ver:
            print(ver)
        #self.tmpImage=i
    def _addName(self,value:str,x:int,y:int,height:int):
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype("./season/standard/ArianaVioleta-dz2K.ttf", height)
        draw.text((x, y),value,(255,255,255),font=font)
    def _addHealth(self,value:int):
        self._addGenericGraphSpec(value=value,x=860,y=2580,w=1300,h=100)
        self._addGenericTextSpec(value=value,x=630,y=2590,h=100)
    def _addAttack(self, value:int):
        self._addGenericGraphSpec(value,860,2780,1300,100)
        self._addGenericTextSpec(value=value,x=630,y=2790,h=100)
    def _addGenericTextSpec(self,value:int,x:int,y:int,h:int):
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype("./season/standard/GalaferaMedium.ttf", h)
        draw.text((x, y),str(value),(255,255,255),font=font)
    def _addGenericGraphSpec(self,value:int,x:int,y:int,w:int,h:int):
        draw = ImageDraw.Draw(self.tmpImage)
        xx=int(value*((w-h)/100))
        draw.ellipse((x+xx, (y), x+xx+h, (y+h)),fill='white')
    def _addSpecials(self,x:int,y:int,yspace:int,h:int):
        print("")
    def _addSerialNumber(self,serial:str,x:int,y:int):
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype("./season/standard/GalaferaMedium.ttf", 70)
        draw.text((x, y),str(serial),'#FFFFFFBC',font=font)

