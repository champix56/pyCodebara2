import signal
from http_core import AsyncHTTPServer
from mysql_core import MySQLClient
import asyncio
import sys
#from codebara import users
from smtp_core import mailto
print(sys.executable)

async def sql():
    sql=MySQLClient()
    await sql.connect()
    ret=await sql.execute('select * from user;')
    print(ret)
    await sql.close()

def main():
    #asyncio.run( sql())
    
    server = AsyncHTTPServer()

    signal.signal(signal.SIGINT, lambda s, f: server.shutdown("SIGINT"))
    signal.signal(signal.SIGTERM, lambda s, f: server.shutdown("SIGTERM"))

    server.run()


if __name__ == "__main__":
    #mailto("","","") 
    main()

    #users.createUser()
