""" image car gen force central image"""
"""from codebara.cards.imageCardCreator import CardImageCreator
from codebara.cards import CardSpecs, SpecialSpec
from codebara.seasons.season import seasonLoader
sSpecs=[SpecialSpec(name="abc"),SpecialSpec(name="def"),]
spec=CardSpecs("Mon premier Codebara", 89,65, sSpecs)
season=seasonLoader()
card = CardImageCreator(uid=23432,season=season )
locfile=card.create(specs=spec, centralImageLoc=None)"""

""" ZIP Compare with one file
import zipfile

zip = zipfile.ZipFile("./stuffBZ2.zip", "w",compression= zipfile.ZIP_BZIP2, compresslevel=9)
zip.write('./c.png')
zip.close()
zip = zipfile.ZipFile("./stuffLZMA.zip", "w",compression= zipfile.ZIP_LZMA, compresslevel=9)
zip.write('./c.png')
zip.close()
zip = zipfile.ZipFile("./stuffDEF.zip", "w",compression= zipfile.ZIP_DEFLATED, compresslevel=9)
zip.write('./c.png')
zip.close()"""