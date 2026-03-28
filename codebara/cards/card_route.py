from aiohttp import web
from codebara.errors import HttpErrors, assembleHttpRequestError, HttpOutputResponse, ResponseStatus
from .cardgen import CardGenerator
#from codebara.tools.common import seededRandom
from codebara.seasons import seasonsFilter
#from codebara.users import UserCoreDatas
from codebara.cards.cardMysql import checkCardIntegrity
from codebara.users.user import renewToken, checkUserTokenValidity, getUserCoreData

import json
async def cardRoutes(request:web.Request,queryArray:tuple,body:dict|None=None)->web.Response:
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_METHOD, request=request)
    header=json.loads(request.headers['datas'])
    validToken=await  checkUserTokenValidity(header['API_TOKEN'],header['API_REQUEST_TOKEN'])
    if validToken is None:
        return assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_TOKEN, request=request).toResponse()
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
            userCodeData=await getUserCoreData(validToken)
            if userCodeData is None:
                return response.toResponse()
            generator = CardGenerator(seasons=seasons, userDatas=userCodeData)
            #print(seededRandom(seed1=6984,seed2= 456))
            try:
                decodedbody=json.loads(body)
                if decodedbody is not None:
                    cb=decodedbody['cb']
                    respgen=await generator.generate(cb=cb)
                    if type(respgen) is int:
                        t={"cardid":respgen}
                        response=HttpOutputResponse(body=t,responseStatus=ResponseStatus.OK)
                    elif type(respgen) is dict:
                        #respgen['API_REQUEST_TOKEN']=t['API_REQUEST_TOKEN']
                        response=HttpOutputResponse(body=respgen, responseStatus=ResponseStatus.Created)
                    else:
                        response=HttpOutputResponse(body=t,responseStatus=ResponseStatus.Internal_Server_Error)
            except Exception as e:
                print(e)
                response=assembleHttpRequestError(error=HttpErrors.ERROR_REQUEST, request=request)
    return  response.toResponseTokenized((await renewToken(validToken))['API_REQUEST_TOKEN'])
