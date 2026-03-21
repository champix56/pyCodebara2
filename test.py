from codebara.cards.cardgen import CardGenerator
#from codebara.users.user import User
from codebara.users.userMysql import getSQLUserCoreDatas
from codebara.seasons.season import seasonsFilter
import asyncio
#from codebara.ThreadPool.Pool import renderPool
import random
def compute_ean13_checksum(code12: str) -> str:
    """
    Calcule le checksum EAN13 à partir des 12 premiers chiffres
    """
    s = 0
    for i, digit in enumerate(code12):
        n = int(digit)
        if i % 2 == 0:
            s += n
        else:
            s += n * 3
    checksum = (10 - (s % 10)) % 10
    return str(checksum)


def random_ean13():
    """
    Génère un code barre EAN13 valide
    """
    code12 = ''.join(str(random.randint(0, 9)) for _ in range(12))
    return code12 + compute_ean13_checksum(code12)

#gen only one card with always same cb
async def cardgen()->str:
    u=await getSQLUserCoreDatas(666)
    seasons=seasonsFilter()
    if u is None:
        return "error"
    else :
        cardgen=CardGenerator(seasons, u)
        return str(await cardgen.generate(cb='64527486384936'))
async def cardgens()->str:
    u=await getSQLUserCoreDatas(666)
    seasons=seasonsFilter()
    if u is None:
        return "error"
    else :
        #return await cardgen.generate(cb='64527486384936')
        for k in range(500):
            u.seed=random.randint(1,6)
            cardgen=CardGenerator(seasons, u)
            print(await cardgen.generate(cb=random_ean13()))
    return 'end'

asyncio.run( cardgen())