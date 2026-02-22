class CardDatas:
    def __init__(self, name):
        self.name = name
    id:int
    creatorId:int
    name:str|None
    imageBlob:str|None
    imageUrl|string|None
    specs:CardSpec

    #seasonMetas
    season:int

    #gendatas
    temporaryId:int|None
    genDate:str
    genTime:float
    startDateTime:str
    cb:str

    #controlDatas
    checksum:str
    currentSign:str

class CardSpec:
    health:int
    primaryAttack:int
    secondariesSpecs: tuple[CardSpeciality]
class CardSpeciality:
    Attack:int|None
    Healt:int|None
    name:str