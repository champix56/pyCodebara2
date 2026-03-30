from aiohttp import web
from codebara.errors import HttpErrors, assembleHttpRequestError, HttpOutputResponse, ResponseStatus
from .cardgen import CardGenerator
#from codebara.tools.common import seededRandom
from codebara.seasons import seasonsFilter
#from codebara.users import UserCoreDatas
from codebara.cards.cardMysql import checkCardIntegrity
from codebara.cards.cardFunction import setCardName, getCardListOfUser, getSingleCardById
from codebara.users.user import renewToken, checkUserTokenValidity, getUserCoreData
from codebara.tools.common import getBase64OfFile
import json
async def cardRoutes(request:web.Request,queryArray:tuple,body:dict|None=None)->web.Response:
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_METHOD, request=request)
    try:
        header=json.loads(request.headers['datas'])
        validToken=await  checkUserTokenValidity(header['API_TOKEN'],header['API_REQUEST_TOKEN'])
        if validToken is None:
            return assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_TOKEN, request=request).toResponse()
        pathSplited=request.path.split('/')
        print(pathSplited)
        match (request.method):
            case ('PUT'):
                match pathSplited[2]:
                    case 'name':
                        decodedbody=json.loads(body)
                        if decodedbody['name']is not None and decodedbody['cid']:
                            card=await setCardName(uid=validToken['id'],  cid=decodedbody['cid'], name=decodedbody['name'])
                            if card is not None:
                                response=HttpOutputResponse(responseStatus=ResponseStatus.OK, body=card)
                            else:
                                response = assembleHttpRequestError(HttpErrors.ERROR_REQUEST, request=request)
                        else :
                            response=assembleHttpRequestError(HttpErrors.ERROR_REQUEST, request=request)
            case ('GET'):
                if len(pathSplited)==2:
                    print('get card id list of connected user')
                    cards=await getCardListOfUser(validToken['id'])
                    response=HttpOutputResponse(body={"cards":cards})
                elif pathSplited[2].isdigit():
                    print("getCard")
                    cardDatas=await getSingleCardById(int(pathSplited[2]))
                    cardDatas['card']=getBase64OfFile(cardDatas['fileloc'])
                    response=HttpOutputResponse(body=cardDatas)
                    # return assembleHttpRequestError(HttpErrors.ERROR_NOT_IMPLEMENTED_YET, request=request)
                else:
                    match pathSplited[2]:
                        case 'check':
                            print('checkcard')
                            datas=json.loads(request.headers['datas'])
                            response=HttpOutputResponse(responseStatus=ResponseStatus.OK, body={"isChecksumGood":await checkCardIntegrity(cid=datas['cid'], hash=datas['hash'])},message="card is OK")
                            print(response)
                    #id=pathSplited[1]
            case ('POST'):
                decodedbody=json.loads(body)
                #if decodedbody is None or decodedbody['cb'] is None:
                #    return assembleHttpRequestError(error= HttpErrors.ERROR_REQUEST,request= request).toResponseTokenized((await renewToken(validToken))['API_REQUEST_TOKEN'])
                cb=decodedbody['cb']
                seasons = seasonsFilter()
                userCodeData=await getUserCoreData(validToken['id'])
                if userCodeData is None:
                    return response.toResponse()
                generator = CardGenerator(seasons=seasons, userDatas=userCodeData)
                #print(seededRandom(seed1=6984,seed2= 456))                respgen=await generator.generate(cb=cb)
                respgen=await generator.generate(cb=cb)
                if type(respgen) is int:
                    t={"cardid":respgen}
                    response=HttpOutputResponse(body=t,responseStatus=ResponseStatus.OK)
                elif type(respgen) is dict:
                    #respgen['API_REQUEST_TOKEN']=t['API_REQUEST_TOKEN']
                    response=HttpOutputResponse(body=respgen, responseStatus=ResponseStatus.Created)
                else:
                    response=HttpOutputResponse(body=t,responseStatus=ResponseStatus.Internal_Server_Error)
        ret=response.toResponseTokenized((await renewToken(validToken['id']))['API_REQUEST_TOKEN'])
    except Exception as e:
        print(e)
        ret=assembleHttpRequestError(error=HttpErrors.ERROR_REQUEST, request=request)
    return ret
