from aiohttp import web
from enum import Enum
import json
from io import StringIO

class ResponseStatus(Enum):
    OK=200
    Internal_Server_Error=500
    Not_Found=404
    Bad_Request=400
    Method_Not_Allowed=405
class HttpErrors(Enum):
    OK=0
    ERROR_SERVER=1
    ERROR_REQUEST=2
    ERROR_INVALID_METHOD=3
    ERROR_INVALID_ROUTE=4

class  HttpOutputResponse():
    def __init__(self,responseStatus:ResponseStatus|None=None, body:dict|None=None,message:str|None=None):
        respStatus=responseStatus if responseStatus is not None else ResponseStatus.Internal_Server_Error
        self.statusText = respStatus.name
        self.status = respStatus.value
        self.ok=False if respStatus.value>=400 else True
    def toJson(self)->str:
        tmpDict={
            "statusText":self.statusText,
            "status":self.status,
            "ok":self.ok,
            "body":self.body,
            "message":self.message
        }
        strtmp=StringIO()
        json.dump(tmpDict,strtmp)
        return strtmp.getvalue()
    statusText:str|None
    status:int
    body:object|str|None
    message:str|None
    ok:bool
    #def toJson(self):
    #    return {"ok":self.ok,"status":self.status,"message":self.message,"body":self.body,"statusText":self.statusText}
    def toResponse(self)->web.Response:
        message:str|None=None if self.body is not None else json.dumps({"message":self.message})
        return web.Response( status=self.status, body=self.body, text=message   , headers=())
        
def assembleHttpRequestError(error:HttpErrors,request: web.Request, message:str|None=None)->HttpOutputResponse:
    retval= HttpOutputResponse()
    status:ResponseStatus|None=None
    requestPathAndMethod="method: "+request.method+" on route:"+request.path
    if error == HttpErrors.ERROR_INVALID_ROUTE or error.value == HttpErrors.ERROR_INVALID_METHOD:
        status=ResponseStatus.Not_Found
        retval.body=None
        retval.message="Invalid Path/Method for: "+requestPathAndMethod
    elif error == HttpErrors.ERROR_REQUEST:
        status=ResponseStatus.Bad_Request
        retval.message="Invalid Request with body given for: "+requestPathAndMethod
        retval.body=None
    # elif error == HttpErrors.ERROR_SERVER:
    else:
        status=ResponseStatus.Not_Found
        retval.message="Invalid Response issue with body given for: "+requestPathAndMethod
        retval.body=None
    text:str=status.name
    retval.statusText=text.replace('_',' ').lower()
    retval.status=status.value    
    retval.ok=False
    if message is not None:
        retval.message+=";"+message
    return retval

"""
def assembleHttpRequest(body:object,status:HttpErrors=HttpErrors.OK)->HttpOutputResponse:
    retval= HttpOutputResponse()
    retval.body=body
    retval.statusText=status.name
    retval.status=status.value
    retval.ok= True if status.value < 400 else False
    retval.message=None
    return retval"""