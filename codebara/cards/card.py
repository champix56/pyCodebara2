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

class CardSpecs:
    name:str
    attack:int
    health:int
    specs:list[SpecialSpec]
    def __init__(self,name:str="",attack:int=0,
                health:int=0,specs:list[SpecialSpec]|None=None):
        self.name=name
        self.attack=attack
        self.health=health
        self.specs=specs if specs is not None else []