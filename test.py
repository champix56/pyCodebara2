from codebara.cards.imageCardCreator import CardImageCreator
import json
from codebara.cards import CardSpecs, SpecialSpec
sSpecs=[SpecialSpec(name="abc"),SpecialSpec(name="def"),]
spec=CardSpecs("Mon premier Codebara", 89,65, sSpecs)
data=None
with open('./season/season.json', "r") as jsonfile:
    data = json.load(jsonfile)
    print(type(data))
    print((data))
card = CardImageCreator(uid=23432,season=data )

card.create(specs=spec)