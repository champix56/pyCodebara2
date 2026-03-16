from mysql_core import MySQLClient
import json
async def register_requestCard(userid:int, request:dict)->int:
    sql=MySQLClient()
    await sql.connect()
    requestJsonText=json.dumps(request)
    sqlReq="INSERT INTO `cdb`.`card_request` (`userid`, `prompt`, `request`, `state`, `fileloc`) VALUES ('666','"+request['prompt']+"', '"+requestJsonText+"', '1', '');"
    res=await sql.nonQuery(sqlReq)
    res=await sql.execute('SELECT last_insert_id() as temporary_request_id;')
    try:
        print(res[0]['temporary_request_id'])
        return res[0]['temporary_request_id']
    except IndexError:
        return -1
async def register_requestCardLocAndHash(userid:int,cardid:str,fileloc:str,hash:str)->None:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="UPDATE `cdb`.`card_request` SET `fileloc`='"+fileloc+"', `cardHash`='"+hash+"' WHERE  `id`="+cardid+";"
    await sql.nonQuery(sqlReq)
async def check_cardHash(cardid:str,hash:str)->bool:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="SELECT id FROM card_request WHERE id="+cardid+" and cardHash='"+hash+"'"
    res=await sql.execute(sqlReq)
    if res[0] is not None:
        return True
    else:
        return False