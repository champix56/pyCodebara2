from aiohttp import web
from codebara.errors import HttpErrors, assembleHttpRequestError
from .card import Card
async def bodyRoute(request:web.Request,body:dict,queryArray:tuple)->web.Response:
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_METHOD, request=request).toResponse()
    match (request.method):
        case ('GET'):
            pathSplited=request.path.split('/')
            
            #id=pathSplited[1]
        case ('POST'):
            # comment: 
            Card.gen('000001')
    return  response
