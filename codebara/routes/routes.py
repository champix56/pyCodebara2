from aiohttp import web
from codebara.errors import assembleHttpRequestError, HttpErrors, HttpOutputResponse
from codebara.cards import  cardRoutes
from codebara.users import userRoutes
async def noBodyRoute(request:web.Request,queryArray:tuple)->web.Response:
    response=assembleHttpRequestError(HttpErrors.ERROR_REQUEST,request=request)
    match request.path.split('/')[1]:
        case 'card':
            response=await cardRoutes(request=request,queryArray=queryArray)
        case 'user':
            response=await userRoutes(request=request,queryArray=queryArray)
    return response
async def bodyRoute(request:web.Request,body:dict,queryArray:tuple)->web.Response:
    if request.path=='/':
        return HttpOutputResponse(message='Hello on codebara').toResponse()
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_ROUTE, request=request).toResponse()
    match request.path.split('/')[1]:
        case 'card':
            response=await cardRoutes(request=request,body=body,queryArray=queryArray)
        case 'user':
            response=await userRoutes(request=request,body=body,queryArray=queryArray)
    return response