from .types import CardDatas
import datetime
import threading
import codebara
class Card(CardDatas):
    temporaryResponse=None
    def __init__(self):
        super.__init__(id=None,creatorId=0)
    @staticmethod
    def gen(cb:str,uid:int=0):
        card=Card()
        card.cb=cb
        card.startDateTime = datetime.datetime.now()
         # Création de 2 threads
        card._threadGen()
        return card
    
    #    def _checkBarcode(self):

    def _threadGen(self):
        return threading.Thread(target=self._internalGen)
    def _internalGen(self):
        response = requests.post(codebara.config.IMAGE_IA_GEN_REST_URL,json=codebara.config.IMAGE_IA_GEN_BODY_BASE)
        # Print the response
        self.temporaryResponse=response.json()
        print(self.temporaryResponse)  
        return self
