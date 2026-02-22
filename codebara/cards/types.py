import random
class CardSpeciality:
    Attack:int|None
    Healt:int|None
    name:str
class CardSpec:
    health:int
    primaryAttack:int
    secondariesSpecs: tuple[CardSpeciality]

class CardDatas:
    def __init__(self,id:int|None,creatorId):
        self.id = id if id is not None else random.randint(0,100000000000000)
        self.creatorId=creatorId
    id:int
    creatorId:int
    name:str|None
    imageBlob:str|None
    imageUrl:str|None
    specs:CardSpec

    #seasonMetas
    season:int

    #gendatas
    temporaryId:int|None
    genDate:str
    genTime:float
    startDateTime:datetime
    cb:str

    #controlDatas
    checksum:str
    currentSign:str
