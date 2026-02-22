from aiohttp import web
from ..errors import HttpOutputResponse, assembleHttpRequestError, HttpErrors
 
async def get(request:web.Request,queryArray)->HttpOutputResponse:
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