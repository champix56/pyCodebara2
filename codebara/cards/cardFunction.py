import json
import tarfile
import os
import shutil
from pathlib import Path
from codebara.tools.common import getSha256FromFile, getBase64OfFile
from codebara.cards.cardMysql import update_registered_requestCard, checkCardOwner, getSQLCardListOfUser, getSQLCardById

def changeCardNameInFile(file:str,name:str):
    with tarfile.open(file) as cardFile:
        print(cardFile.getnames())
        fileNameSplit=file.split('/')
        repfolder='./tmp/untar/'+fileNameSplit[len(fileNameSplit)-1][:-4]
        if Path(repfolder).exists():
            shutil.rmtree(repfolder)
        Path(repfolder).mkdir(parents=True)
        cardFile.extractall(repfolder)
        cardFile.close()
        datas=None
        with open(repfolder+'/datas.json') as datasJson:
            datas=json.load(datasJson)
            datas['name']=name
            datasJson.close()
        with open(repfolder+'/datas.json',"w") as fout:
            json.dump(datas, fout)
            fout.close()
        with open(repfolder+'/hashs.json') as datasJson:
            datas=json.load(datasJson)
            datas['datas']=getSha256FromFile(repfolder+'/datas.json')
            datasJson.close()
        with open(repfolder+'/hashs.json',"w") as fout:
            json.dump(datas, fout)
        os.remove(file)
        with tarfile.open( file, "w:xz") as tar:
            for name in os.listdir( repfolder ):
                #if not name.endswith('card.tar.gz'):
                tar.add(repfolder+'/'+name, arcname=name)
                os.remove(repfolder+'/'+name)
        shutil.rmtree(repfolder)
        tar.close()
async def setCardName(uid:int,cid:int,name:str)->dict|None:
    fileloc=await checkCardOwner(uid,cid)
    if fileloc is not None:
        changeCardNameInFile(file=fileloc,name=name)
        await update_registered_requestCard(ownerid=uid, cardid=cid,name=name, hash=getSha256FromFile(fileloc))
        return {"cid":cid,"card":getBase64OfFile(fileLoc=fileloc)}
    else:
        return None
async def getCardListOfUser(uid:int)->list:
    return await getSQLCardListOfUser(uid)
async def getSingleCardById(cid:int):
    return await getSQLCardById(cid)
