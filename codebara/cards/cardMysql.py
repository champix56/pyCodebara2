from mysql_core import MySQLClient
from codebara.cards.card import CardSpecs
import json
async def register_requestCard(userid:int, request:dict, seasonid:int)->int:
    sql=MySQLClient()
    await sql.connect()
    requestJsonText=json.dumps(request)
    sqlReq="INSERT INTO `cdb`.`card` (`ownerid`,`creatorid`,`seasonid`, `prompt`, `request`, `state`) VALUES ("+str(userid)+","+str(userid)+","+str(seasonid)+",'"+request['prompt']+"', '"+requestJsonText+"', '0');"
    res=await sql.nonQuery(sqlReq)
    res=await sql.execute('SELECT last_insert_id() as temporary_request_id;')
    await sql.close()
    try:
        print(res[0]['temporary_request_id'])
        return res[0]['temporary_request_id']
    except IndexError:
        return -1
async def update_registered_requestCard(cardid:str,ownerid:int|None=None,fileloc:str|None=None,hash:str|None=None,specs:CardSpecs|None=None)->None:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="UPDATE `cdb`.`card` SET "
    if fileloc is not None:
        sqlReq+="`fileloc`='"+fileloc+"',"
    if ownerid is not None:
        sqlReq+="`ownerid`="+str(ownerid)+","
    if specs is not None:
        sqlReq+="`power`="+str(specs.power)+", `name`='"+specs.name+"', `health`="+str(specs.health)+", `attack`="+str(specs.attack)+","
    sqlReq+="`cardHash`='"+hash+"', `state`=1 WHERE  `id`="+str(cardid)+";"
    await sql.nonQuery(sqlReq)
    await sql.close()
async def check_cardHash(cardid:str,hash:str)->bool:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="SELECT id FROM  `cdb`.`card` WHERE id="+str(cardid)+" and cardHash='"+hash+"'"
    res=await sql.execute(sqlReq)
    await sql.close()
    if len(res)>0:
        return True
    else:
        return False
    
    
    
    
    
    
async def checkCardIntegrity(cid:int, hash:str)-> bool:
   resp=await check_cardHash(cardid=cid, hash=hash)
   return resp