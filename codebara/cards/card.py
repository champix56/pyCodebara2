class SpecialSpec:
    name:str
    attack:int=0
    health:int=0
    turn:int=-1

class CardSpecs:
    name:str
    attack:int
    health:int
    specs:list[SpecialSpec]|None
    def __init__(self,name:str="",attack:int=0,
                health:int=0,specs=None):
        self.name=name
        self.attack=attack
        self.health=health
        self.specs=specs