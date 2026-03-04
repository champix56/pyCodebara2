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