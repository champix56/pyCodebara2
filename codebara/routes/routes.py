from aiohttp import web
from ..errors import assembleHttpRequestError, HttpErrors
from codebara.cards import  cardBodyRoute
async def noBodyRoute(request:web.Request,queryArray:tuple)->web.Response:
    return web.Response()
async def bodyRoute(request:web.Request,body:dict,queryArray:tuple)->web.Response:
    response=assembleHttpRequestError(error=HttpErrors.ERROR_INVALID_ROUTE, request=request).toResponse()
    if request.path.startswith('/card'):
        response=await cardBodyRoute(request=request,body=body,queryArray=queryArray)
    return response
"""async def get(request:web.Request,queryArray)->HttpOutputResponse:
    return HttpOutputResponse()
async def post(request:web.Request,body,queryArray)->HttpOutputResponse:
    print(request.method+":"+request.path+"\r\nbody :")
    print(request.post)
    error  = assembleHttpRequestError(HttpErrors.OK,request=request)
    #print( error)
    return error
async def put(request:web.Request,body,queryArray)->HttpOutputResponse:
    return HttpOutputResponse()
async def patch(request:web.Request,body,queryArray)->HttpOutputResponse:
    return HttpOutputResponse()
async def delete(request:web.Request,body,queryArray)->HttpOutputResponse:
    return HttpOutputResponse()
"""