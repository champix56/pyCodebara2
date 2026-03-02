from aiohttp import web
from codebara.errors import HttpErrors, assembleHttpRequestError
from .cardgen import CardGenerator
async def cardBodyRoute(request:web.Request,body:dict,queryArray:tuple)->web.Response:
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_METHOD, request=request)
    match (request.method):
        case ('GET'):
            pathSplited=request.path.split('/')
            print(pathSplited)
            #id=pathSplited[1]
        case ('POST'):
            # comment: 
            generator = CardGenerator(cb="123", uid=0)
            print(CardGenerator.seededRandom(seed1=6984,seed2= 456))
            generator.generate()
    return  response.toResponse()
