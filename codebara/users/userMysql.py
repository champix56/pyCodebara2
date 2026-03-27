from enum import Enum, IntFlag
from mysql_core import MySQLClient
from .user import UserCoreDatas
from codebara.tools.common import  str_random, getSha256OfStr
async def getSQLUserCoreDatas(uid:int)->UserCoreDatas|None:
    sql=MySQLClient()
    await sql.connect()
    user=await sql.execute('SELECT id, seed, hash from user where id='+str(uid))
    try:
        return UserCoreDatas(uid= user[0]['id'], seed=user[0]['seed'], hash=user[0]['hash'])
    except IndexError :
        return None
async def createSQLUser(mail:str, password:str)->dict|None:
    sql=MySQLClient()
    await sql.connect()
    apiToken=getSha256OfStr(mail+ str_random(64)+password)
    requestToken=getSha256OfStr(password+ str_random(64))
    sqlReq = "INSERT INTO `cdb`.`user` (`mail`, `password`, `nickname`, `API_token`, `API_request_token`) VALUES ('"+mail+"',SHA2('"+mail+password+"',256),'"+mail+"', '"+apiToken+"', '"+requestToken+"');"
    res = await sql.nonQuery(sqlReq)
    res = await sql.execute("SELECT last_insert_id() as temporary_request_id;")
    await sql.close()
    try:
        print('created:'+str(res[0]["temporary_request_id"]))
        return {"API_TOKEN":apiToken, "API_REQUEST_TOKEN":requestToken}
    except IndexError:
        return None
"""async def getHashOfUser(mail:str)->str|None:
    sql=MySQLClient()
    await sql.connect()
    sqlReq = "SELECT (`hash`) FROM `user` WHERE `mail`='mail';"
    res = await sql.execute(sqlReq)
    await sql.close()
    if(len(res)>0):
        return res[0]['hash']
    else:
        return None"""
class TokenTypes(IntFlag):
    API_TOKEN=1<<0
    API_REQUEST_TOKEN=1<<1
    API_BOTH=1<<0&1<<1
async def resetTokens(uid:int,tokenTypes: TokenTypes=TokenTypes.API_BOTH ):#->dict|None:
    ret={}
    sqlReq="UPDATE user SET "
    if tokenTypes&TokenTypes.API_TOKEN:
        apiToken=getSha256OfStr(str_random(64))
        sqlReq+="`API_token`='"+apiToken+"' "
        ret['API_TOKEN']=apiToken
    if tokenTypes&TokenTypes.API_BOTH:
        sqlReq+=' AND '
    if tokenTypes&TokenTypes.API_REQUEST_TOKEN:
        apirequestToken=getSha256OfStr(str_random(64))
        sqlReq+="`API_request_token`='"+apirequestToken+"' "
        ret['API_REQUEST_TOKEN']=apirequestToken
    sqlReq+=" WHERE `id`="+str(uid)+";"
    try:
        sql=MySQLClient()
        await sql.connect()
        await sql.nonQuery(sqlReq)
        await sql.close()
        return ret
    except Exception as e:
        print(e)
        return None
async def authSqlUser(mail:str,hashedPassword:str)->dict|None:
    sql=MySQLClient()
    await sql.connect()
    sqlReq = "SELECT (`id`) FROM `user` WHERE `mail`='mail' and `password`='"+hashedPassword+"';"
    res = await sql.execute(sqlReq)
    await sql.close()
    if(len(res)>0):
        id=res[0]['id']
        return await resetTokens(id)
    else:
        return None
async def authUserSQLByTokens(apiToken:str,requestToken:str)->dict|None:
    sql=MySQLClient()
    await sql.connect()
    sqlReq="SELECT `id` FROM `user` WHERE `API_token`='"+apiToken+"' and `API_request_token`='"+requestToken+"';"
    res=await sql.execute(sqlReq)
    await sql.close()
    if len(res)>0:
        id=res[0]['id']
        return await resetTokens(id)
    else:
        return None