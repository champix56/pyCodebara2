from aiohttp import web
from codebara.errors import HttpErrors, assembleHttpRequestError, HttpOutputResponse, ResponseStatus
from .cardgen import CardGenerator
#from codebara.tools.common import seededRandom
from codebara.seasons import seasonsFilter
from codebara.users import UserCoreDatas
from codebara.cards.cardMysql import checkCardIntegrity

import json
async def cardRoutes(request:web.Request,queryArray:tuple,body:dict|None=None)->web.Response:
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_METHOD, request=request)
    match (request.method):
        case ('GET'):
            pathSplited=request.path.split('/')
            print(pathSplited)
            if pathSplited[2].isdigit():
                print("getCard")
                return assembleHttpRequestError(HttpErrors.ERROR_NOT_IMPLEMENTED_YET, request=request)
            else:
                match pathSplited[2]:
                    case 'check':
                        print('checkcard')
                        try:
                            datas=json.loads(request.headers['datas'])
                            response=HttpOutputResponse(responseStatus=ResponseStatus.OK, body={"isChecksumGood":await checkCardIntegrity(cid=datas['cid'], hash=datas['hash'])},message="card is OK")
                            print(response)
                        except KeyError as e:
                            print(e)
                            response=assembleHttpRequestError(error=HttpErrors.ERROR_REQUEST, request=request)
                #id=pathSplited[1]
        case ('POST'):
            # comment: 
            seasons = seasonsFilter()
            generator = CardGenerator(seasons=seasons, userDatas=UserCoreDatas(uid=666, seed= 6,hash=''))
            #print(seededRandom(seed1=6984,seed2= 456))
            try:
                if body is not None:
                    cb=body['cb']
                    await generator.generate(cb=cb)
            except Exception as e:
                print(e)
                response=assembleHttpRequestError(error=HttpErrors.ERROR_REQUEST, request=request)
    return  response.toResponse()
