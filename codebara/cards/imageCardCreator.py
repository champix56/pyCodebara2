
import random
from codebara.seasons.season import seasonLoader
from PIL import Image, ImageDraw, ImageFont

from codebara.cards.card import CardSpecs, SpecialSpec
#from codebara.cards.cardgen import CardGenerator
from codebara.tools.common import seededRandom
DEBUG=True
class Location2D:
    x: int
    y: int
    h: int
    w: int
    color: str

    def __init__(self, x: int, y: int, w: int, h: int, color: str = "#FFFFFF"):

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color


class Location1D:
    x: int
    y: int
    h: int
    color: str

    def __init__(self, x, y, color: str = "#FFFFFF", h: int | None = 1):
        self.x = x
        self.y = y
        self.h = h
        self.color = color


class CardImageCreator:
    id: int
    creatorid: int
    specs: CardSpecs
    season: dict
    seasonId: int
    outCardHeight: int
    outCardWidth: int
    # positions
    healthBarLoc: Location2D | None
    healthValueLoc: Location1D
    attackValueLoc: Location1D
    attackBarLoc: Location2D | None
    nameLoc: Location1D
    serialLoc: Location1D
    imageLoc: Location2D
    specialsSpecLoc: Location1D

    seasonRessourcesFolder: str
    outLoc: str
    tmpImage: Image.Image

    def __init__(self, uid=0, season: dict | None = None):  # outw=2370(1185),outh=4096(2048)):
        self.id = int(
            random.random()
            * 100000
            * seededRandom(1000, int(random.random() * 1000))
        )
        self.creatorid = uid
        """if specs is None:
            self.specs = CardSpecs()
        else:
            self.specs = specs"""
        if season is None:
            self.season = seasonLoader()
        else:
            self.season = season
        self.seasonId = self.season["seasonid"]
        self.outCardWidth = self.season["deck"]["width"]  # outw
        self.outCardHeight = self.season["deck"]["height"]  # outh
        tempSection = None
        try:
            tempSection = self.season["deck"]["positions"]["healthbar"]
            self.healthBarLoc = Location2D(
                x=tempSection["x"],
                y=tempSection["y"],
                w=tempSection["width"],
                h=tempSection["height"],
                color=tempSection["color"],
            )
        except KeyError:
            self.healthBarLoc = None
        try:
            tempSection = self.season["deck"]["positions"]["attackbar"]
            self.attackBarLoc = Location2D(
                x=tempSection["x"],
                y=tempSection["y"],
                w=tempSection["width"],
                h=tempSection["height"],
                color=tempSection["color"],
            )
        except KeyError:
            self.attackBarLoc = None
        tempSection = self.season["deck"]["positions"]["health"]
        self.healthValueLoc = Location1D(
            x=tempSection["x"],
            y=tempSection["y"],
            h=tempSection["height"],
            color=tempSection["color"],
        )
        tempSection = self.season["deck"]["positions"]["attack"]
        self.attackValueLoc = Location1D(
            x=tempSection["x"],
            y=tempSection["y"],
            h=tempSection["height"],
            color=tempSection["color"],
        )
        tempSection = self.season["deck"]["positions"]["name"]
        self.nameLoc = Location1D(
            x=tempSection["x"],
            y=tempSection["y"],
            h=tempSection["height"],
            color=tempSection["color"],
        )
        tempSection = self.season["deck"]["positions"]["id"]
        self.serialLoc = Location1D(
            x=tempSection["x"],
            y=tempSection["y"],
            h=tempSection["height"],
            color=tempSection["color"],
        )
        tempSection = self.season["deck"]["positions"]["image"]
        self.imageLoc = Location2D(
            x=tempSection["x"],
            y=tempSection["y"],
            h=tempSection["height"],
            w=tempSection["width"],
            color=tempSection["color"],
        )
        tempSection = self.season["deck"]["positions"]["special"]
        self.specialsSpecLoc = Location1D(
            x=tempSection["x"],
            y=tempSection["y"],
            h=tempSection["height"],
            color=tempSection["color"],
        )
        self.outLoc = "/" + str(self.id)

    def _resizeAndSave(self,)->str:
        self.tmpImage.thumbnail((1185,2048), Image.Resampling.LANCZOS)
        #self.tmpImage=self.tmpImage.convert('RGB')
        outputFileName="." + self.outLoc+ ".png"
        self.tmpImage.save(outputFileName, "PNG",quality=1)
        print(outputFileName)
        return outputFileName
    def create(self, specs: CardSpecs, centralImageLoc:str)->str:
        self.outputFormat=format
        self.specs = specs
        self._createEmptyBase("./season/standard/front.png")
        self._addPerso(loc=centralImageLoc)# if DEBUG is True and centralImageLoc is not None else "./season/beta/2.png")
        self._addName()
        self._addAttack()
        self._addHealth()
        self._addSpecials()
        self._addSerialNumber(
            serial=str(self.id) + "-" + str(self.seasonId) + "-" + str(self.creatorid),
        )
        """self.tmpImage.save("." + self.outLoc)
        print("." + self.outLoc)"""
        outputFileName=self._resizeAndSave()
        self.tmpImage.close()
        return outputFileName

    def _createEmptyBase(self, deckloc: str):
        im = Image.new("RGBA", (self.outCardWidth, self.outCardHeight))
        try:
            with Image.open(deckloc) as im2:
                rgba = im2.convert("RGBA")
                print(deckloc, im.format, f"{im.size}x{im.mode}")
                print(deckloc, im2.format, f"{im2.size}x{im2.mode}")
                im.paste(rgba, (0, 0, im2.size[0], im2.size[1]))
        except OSError as e:
            print(e)
        self.tmpImage = im
        return self.outLoc

    def _addPerso(
        self, loc: str, x: int = 108, y: int = 367, w: int = 2151, h: int = 1981
    ):
        i = self.tmpImage
        persoIm = Image.open(loc).convert("RGBA")
        persoImg = persoIm.resize((w, h)).convert("RGBA")
        try:
            i.paste(persoImg, (x, y))
        except ValueError as ver:
            print(ver)
        # self.tmpImage=i

    def _addName(self):
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype(
            "./season/standard/ArianaVioleta-dz2K.ttf", float(str(self.nameLoc.h))
        )
        draw.text(
            (self.nameLoc.x, self.nameLoc.y),
            self.specs.name,
            self.nameLoc.color,
            font=font,
        )

    def _addHealth(self):
        self._addGenericTextSpec(
            value=self.specs.health,
            x=self.healthValueLoc.x,
            y=self.healthValueLoc.y,
            h=(self.healthValueLoc.h if self.healthValueLoc.h is not None else 0),
            color=self.healthValueLoc.color,
        )
        if self.healthBarLoc is not None:
            self._addGenericGraphSpec(
                value=self.specs.health,
                x=self.healthBarLoc.x,
                y=self.healthBarLoc.y,
                w=self.healthBarLoc.w,
                h=self.healthBarLoc.h + 2,
                color=self.healthBarLoc.color,
            )

    def _addAttack(self):
        self._addGenericTextSpec(
            value=self.specs.attack,
            x=self.attackValueLoc.x,
            y=self.attackValueLoc.y,
            h=(self.attackValueLoc.h if self.attackValueLoc.h is not None else 0),
            color=self.attackValueLoc.color,
        )
        if self.attackBarLoc is not None:
            self._addGenericGraphSpec(
                self.specs.attack,
                self.attackBarLoc.x,
                self.attackBarLoc.y,
                self.attackBarLoc.w,
                self.attackBarLoc.h + 2,
                self.attackBarLoc.color,
            )

    def _addGenericTextSpec(
        self, value: int, x: int, y: int, h: int, color: str = "WHITE"
    ):
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype("./season/standard/GalaferaMedium.ttf", h)
        draw.text((x, y), str(value), color, font=font)

    def _addGenericGraphSpec(
        self, value: int, x: int, y: int, w: int, h: int, color: str = "BLUE"
    ):
        draw = ImageDraw.Draw(self.tmpImage)
        xx = int(value * ((w - h) / 100))
        draw.ellipse((x + xx, (y), x + xx + h, (y + h)), fill=color)

    def _addSpecials(self):
        positionY = self.specialsSpecLoc.y
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype(
            "./season/standard/GalaferaMedium.ttf", float(str(self.specialsSpecLoc.h))
        )
        for spec in self.specs.specs:
            self._printSpecialSpec(
                draw=draw, spec=spec, x=self.specialsSpecLoc.x, y=positionY, color=self.specialsSpecLoc.color, font=font
            )
            #draw.text(xy=(self.specialsSpecLoc.x, positionY),text=spec.name,color=self.specialsSpecLoc.color,font=font)
            positionY += self.specialsSpecLoc.h + 20

    def _printSpecialSpec(
        self,
        draw: ImageDraw.ImageDraw,
        spec: SpecialSpec,
        x: int,
        y: int,
        color: str,
        font: ImageFont.FreeTypeFont,
    ):
        draw.text(
            (x, y),
            spec.name,
            color,
            font=font,
        )

    def _addSerialNumber(self, serial: str):
        draw = ImageDraw.Draw(self.tmpImage)
        font = ImageFont.truetype(
            "./season/standard/GalaferaMedium.ttf", float(str(self.serialLoc.h))
        )
        draw.text(
            (self.serialLoc.x, self.serialLoc.y),
            str(serial),
            self.serialLoc.color,
            font=font,
        )
