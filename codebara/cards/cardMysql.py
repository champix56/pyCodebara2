import json

from codebara.cards.card import CardSpecs
from mysql_core import MySQLClient


async def register_requestCard(userid: int, request: dict, seasonid: int) -> int:
    sql = MySQLClient()
    await sql.connect()
    requestJsonText = json.dumps(request)
    sqlReq = (
        "INSERT INTO `cdb`.`card` (`ownerid`,`creatorid`,`seasonid`, `prompt`, `request`, `state`) VALUES ("
        + str(userid)
        + ","
        + str(userid)
        + ","
        + str(seasonid)
        + ",'"
        + request["prompt"]
        + "', '"
        + requestJsonText
        + "', '0');"
    )
    res = await sql.nonQuery(sqlReq)
    res = await sql.execute("SELECT last_insert_id() as temporary_request_id;")
    await sql.close()
    try:
        print(res[0]["temporary_request_id"])
        return res[0]["temporary_request_id"]
    except IndexError:
        return -1


async def update_registered_requestCard(
    cardid: int,
    ownerid: int | None = None,
    fileloc: str | None = None,
    hash: str | None = None,
    specs: CardSpecs | None = None,
    name:str|None=None
) -> None:
    sql = MySQLClient()
    await sql.connect()
    sqlReq = "UPDATE `cdb`.`card` SET "
    if fileloc is not None:
        sqlReq += "`fileloc`='" + fileloc + "',"
    if name is not None:
        sqlReq += "`name`='" + name + "',"
    if ownerid is not None:
        sqlReq += "`ownerid`=" + str(ownerid) + ","
    if specs is not None:
        sqlReq += (
            "`power`="
            + str(specs.power)
            + ", `name`='"
            + specs.name
            + "', `health`="
            + str(specs.health)
            + ", `attack`="
            + str(specs.attack)
            + ","
        )
    sqlReq += "`cardHash`='" + hash + "', `state`=1 WHERE  `id`=" + str(cardid) + ";"
    await sql.nonQuery(sqlReq)
    await sql.close()


async def check_cardHash(cardid: int, hash: str) -> bool:
    sql = MySQLClient()
    await sql.connect()
    sqlReq = (
        "SELECT id FROM  `cdb`.`card` WHERE id="
        + str(cardid)
        + " and cardHash='"
        + hash
        + "'"
    )
    res = await sql.execute(sqlReq)
    await sql.close()
    if len(res) > 0:
        return True
    else:
        return False


async def checkCardIntegrity(cid: int, hash: str) -> bool:
    resp = await check_cardHash(cardid=cid, hash=hash)
    return resp


async def checkCardOwner(uid: int, cid: int) -> str|None:
    sql = MySQLClient()
    await sql.connect()
    sqlReq = (
        "SELECT `fileloc` FROM  `cdb`.`card` WHERE ownerid="
        + str(uid)
        + " and id="
        + str(cid)
        + ";"
    )
    res = await sql.execute(sqlReq)
    await sql.close()
    if len(res) > 0:
        return res[0]['fileloc']
    else:
        return None
