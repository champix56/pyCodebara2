from codebara.tools.common import str_random
from .user_types import UserCoreDatas
from .userMysql import createSQLUser, authSqlUser, resetTokens, TokenTypes, authUserSQLByTokens,checkUserSQLTokensValidity, getSQLUserCoreDatas
from smtp_core.smtp import mailto
from codebara.config.debug import DEBUG
async def createUser(mail:str)->dict|None:
    password=str_random(15)
    apitoken=(await createSQLUser(mail=mail, password=password))
    if DEBUG is not True:
        mailto(mail,'Codebara user :'+str(id)+' password : '+password,'CODEBARA password for user '+mail)
    return apitoken
async def refreshTokens(uid:int, tokenType:TokenTypes=TokenTypes.API_BOTH):
    return resetTokens(uid=uid, tokenTypes=tokenType)
async def authUser(mail:str,hashedPass:str)->dict|None:
    return await authSqlUser(mail=mail,hashedPassword=hashedPass)
async def authUserByTokens(apitoken:str, requesttoken:str)->dict|None:
    return await authUserSQLByTokens(apiToken=apitoken, requestToken=requesttoken)
async def checkUserTokenValidity(apitoken:str, requesttoken:str)->int|None:
    return await checkUserSQLTokensValidity(apiToken=apitoken,requestToken=requesttoken )
async def getUserCoreData(uid:int)->UserCoreDatas|None:
    return await getSQLUserCoreDatas(uid)
async def renewToken(uid:int)->dict:
    return await resetTokens(uid,TokenTypes.API_REQUEST_TOKEN)