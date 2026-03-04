from mysql_core import MySQLClient
from .user import UserCoreDatas
async def getSQLUserCoreDatas(uid:int)->UserCoreDatas|None:
    sql=MySQLClient()
    await sql.connect()
    user=await sql.execute('SELECT id, seed from user where id='+str(uid))
    try:
        return UserCoreDatas(uid= user[0]['id'], seed=user[0]['seed'])
    except IndexError :
        return None