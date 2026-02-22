from .types import CardDatas
import datetime
class Card(CardDatas):
    temporaryResponse=None
    @staticmethod
    def gen(cb:str):
        card=Card()
        card.cb=cb
        card.startDateTime = datetime.datetime.now()
         # Création de 2 threads
        thread = threading.Thread(card._internalGen) 
        return card
    
    def _internalGen(self):
        response = requests.post(url, json=data)
        # Print the response
        self.temporaryResponse=response.json()
        print(self.temporaryResponse)  
        return self
