from codebara.tools.common import str_random
from .userMysql import createSQLUser, authSqlUser, resetTokens, TokenTypes, authUserSQLByTokens
from smtp_core.smtp import mailto
class UserCoreDatas:
    def __init__(self, uid: int, seed: int,hash :str):
        self.uid = uid
        self.seed = seed
        self.hash=hash
        self.serverDataLoc='./contents/user/'+str(uid)

class User(UserCoreDatas):
    def __init__(self, uid: int, seed: int,hash:str, nickname: str, mail: str, amount: int):
        super().__init__(uid, seed,hash)
        self.mail = mail
        self.nickname = nickname
        self.amount = amount
    def parentInstance(self)->UserCoreDatas:
        return UserCoreDatas(self.uid,self.seed,self.hash)
async def createUser(mail:str)->dict|None:
    password=str_random(15)
    apitoken=(await createSQLUser(mail=mail, password=password))
    mailto(mail,'Codebara user :'+str(id)+' password : '+password,'CODEBARA password for user '+mail)
    return apitoken
async def refreshTokens(uid:int, tokenType:TokenTypes=TokenTypes.API_BOTH):
    return resetTokens(uid=uid, tokenTypes=tokenType)
async def authUser(mail:str,hashedPass:str)->dict|None:
    return await authSqlUser(mail=mail,hashedPassword=hashedPass)
async def authUserByTokens(apitonken:str, requesttoken:str)->dict|None:
    return await authUserSQLByTokens(apiToken=apitonken, requestToken=requesttoken)