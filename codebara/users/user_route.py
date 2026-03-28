from aiohttp import web
import json
from codebara.errors import HttpErrors, assembleHttpRequestError, HttpOutputResponse, ResponseStatus
from codebara.users import authUser, authUserSQLByTokens, createUser
async def userRoutes(request:web.Request,queryArray:tuple,body:dict|None=None)->web.Response:
    try:
        response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_METHOD, request=request)
        pathSplited=request.path.split('/')
        print(pathSplited)
        match (request.method):
            case ('GET'):
                if len(pathSplited)>2 and pathSplited[2].isdigit():
                    print("getUserDatas for all")
                    #return assembleHttpRequestError(HttpErrors.ERROR_NOT_IMPLEMENTED_YET, request=request)
                else:
                    match pathSplited[2]:
                        case 'auth':
                            datas=json.loads(request.headers['datas'])
                            if datas['API_TOKEN'] is not None and datas['API_REQUEST_TOKEN'] is not None:
                                #auth by token
                                #response=HttpOutputResponse(responseStatus=ResponseStatus.OK, body={"isChecksumGood":await checkCardIntegrity(cid=datas['cid'], hash=datas['hash'])},message="card is OK")
                                tokens=await authUserSQLByTokens(datas['API_TOKEN'], datas['API_REQUEST_TOKEN'])
                                if tokens is not None:
                                    response=HttpOutputResponse(body=tokens)
                                    print('API AUTH')
                            elif datas['mail'] is not None and datas['pass'] is not None:
                                #auth by log/pass
                                print("auth LOG/PASS")
                                tokens=await authUser(datas['mail'], datas['pass'])
                                if tokens is not None:
                                    response=HttpOutputResponse(body=tokens)
                                
            case ('POST'):
                if request.path=='/user':
                    #creation de user
                    print("create user")
                    if body is not None:
                        decodeBody=json.loads(body)
                        tokens=await createUser(decodeBody['mail'])
                        response=HttpOutputResponse(body=tokens)
                else:
                    print('other post')
        return  response.toResponse()
    except Exception as e:
        print(e)
        return assembleHttpRequestError(error=HttpErrors.ERROR_REQUEST, request=request)
