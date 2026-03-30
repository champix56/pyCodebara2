import json
#from io import TextIOWrapper
#from codebara.cards.cardMysql import check_cardHash
class SpecialSpec:
    name:str
    attack:int=0
    health:int=0
    turn:int=-1
    def __init__(self, name, attack:int=0,health:int=0, turn:int=-1):
        self.name = name
        self.attack=attack
        self.health=health
        self.turn=turn
    def toJson(self)->str:
        return json.dumps(self.__dict__)
class CardSpecs:
    id:int
    name:str
    attack:int
    health:int
    power:int=100
    rarity:float=1.0
    specials:list[SpecialSpec]
    def __init__(self,cid:int,name:str="",attack:int=0,
                health:int=0,specials:list[SpecialSpec]|None=None,power:int=100, rarity:float=1.0):
        self.name=name
        self.attack=attack
        self.health=health
        self.rarity=rarity
        self.power=power
        self.id=cid
        self.specials=specials if specials is not None else []
    def todict(self)->dict:
        tempDictSpecs=[]
        for spec in self.specials:
            tempDictSpecs.append(spec.__dict__)
        return {
            "id":self.id,
            "name":self.name,
            "attack":self.attack,
            "health":self.health,
            "rarity":self.rarity,
            "power":self.power,
            "specials":tempDictSpecs }
    def toJson(self)->str:
        return json.dumps(self.todict())
class Card (CardSpecs):
    id:int
    ownerid:int
    creatorid:int
    imageFileName:str
    centralImageFileName:str
    promptid:str
    seasonid:int
    seed:int
    def __init__(self,id:int,seasonid:int,promptid:str,seed:int,ownerid:int,creatorid:int,name:str,imageFilename:str,centralImageFilename:str,attack:int=0,
                health:int=0,specs:list[SpecialSpec]|None=None):
        super().__init__(id,name,attack,health,specs)
        self.id=id
        self.seed=seed
        self.creatorid=creatorid
        self.ownerid=ownerid
        self.seasonid=seasonid
        self.centralImageFileName=centralImageFilename
        self.imageFileName=imageFilename
        self.promptid=promptid

    def toJson(self):
        return json.dumps(self.__dict__)
    def toCardSpecs(self):
        return super().toJson()