#from PIL import Image
from codebara.cards import Card
import hashlib
from codebara.tools import getSha256OfStr
"""import base64

sample_string = "GeeksForGeeks is the best"
sample_string_bytes = sample_string.encode("ascii")

base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")

print(f"Encoded string: {base64_string}")"""
"""from codebara.seasons import seasonsFilter
print(seasonsFilter())"""
#test redim
"""img=Image.open('./carte.png')
img=img.resize((int(img.width/2.2),int(img.height/2.2)))
img.save('./carteL.png',format='PNG', optimize=True)"""

card=Card(promptid='000',id=0,seed=1, name="",ownerid=666,creatorid=666, seasonid=1, imageFilename='000.png', centralImageFilename='000.png')
print(card.toJson())
print(card.toCardSpecs())
h = hashlib.new('sha256')
h.update(b"godmdp")
h.hexdigest()
print(h.hexdigest())

print('by function :')
print (getSha256OfStr("godmdp"))