from mysql_core import MySQLClient
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
async def register_requestCardLocAndHash(userid:int,cardid:str,fileloc:str,hash:str)->None:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="UPDATE `cdb`.`card` SET `fileloc`='"+fileloc+"',`state`=1, `cardHash`='"+hash+"' WHERE  `id`="+str(cardid)+";"
    await sql.nonQuery(sqlReq)
    await sql.close()
async def check_cardHash(cardid:str,hash:str)->bool:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="SELECT id FROM  `cdb`.`card` WHERE id="+cardid+" and cardHash='"+hash+"'"
    res=await sql.execute(sqlReq)
    await sql.close()
    if res[0] is not None:
        return True
    else:
        return False