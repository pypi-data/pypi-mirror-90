


from .body import AsueRequestBody
from .params import AsueRequestParams
from .headers import AsueRequestHeaders 
from .response import AsueRequestResponse
from ..template.useful import decode_data, encode_data
import asyncio
import json
from json.decoder import JSONDecodeError
            

class AsueRequestObject:
    
    def __init__(self, scope :dict, receive :callable, send :callable):
           
        self.path = self.get_path(scope=scope)
        self.method = self.get_method(scope=scope) 
        self.responser = AsueRequestResponse(send=send)  
        self.coroutine(function=self.read_body(receive=receive)) 
        self.params = AsueRequestParams(params=self.get_params(scope=scope))      
        self.headers = AsueRequestHeaders(headers=self.get_headers(scope=scope))         
              
           
    def get_responser(self, send):
        return send
    
    def get_path(self, scope):
        return scope['path']
    
    def get_method(self, scope):
        return scope['method']
        
    def get_headers(self, scope):       
        headers = scope['headers']    
        decodeds = []
        for item in headers:       
            item = (decode_data(item[0]), decode_data(item[1]))        
            decodeds.append(item)        
        newl = {}
        for item in decodeds:        
            newl.update({item[0] : item[1]})                                      
        return newl
    
    
    def get_params(self, scope):       
        params = decode_data(scope['query_string'])    
        params = params.split('&')       
        aux = []    
        for item in params:        
            aux.append(item.split('='))        
        newl = {}    
        for item in aux:        
            if len(item)>1:            
                newl.update({item[0] : item[1]})                 
        return newl
        
        
    async def read_body(self, receive):        
        body = b''        
        more_body = True       
        while more_body:        
            message = await receive()         
            body += message.get('body', b'')          
            more_body = message.get('more_body', False)
        nBody = ''
        try:                   
            nBody = json.loads(body)   
        except JSONDecodeError:
            pass
        self.body = AsueRequestBody(body=nBody) 
          
    
    def coroutine(self, function):
        loop = asyncio.new_event_loop()     
        asyncio.set_event_loop(loop)        
        loop.run_until_complete(function) 
    

    def get_json(self):
        newd = self.__dict__
        headers = newd['headers']
        params = newd['params']
        body = newd['body']
        newd['headers'] = headers.get_json()
        newd['params'] = params.get_json()
        newd['body'] = body.get_json()    
        newdd = {}
        for item in newd.items():
            newdd.update({item[0]: item[1]})         
        del newdd['responser']
        return json.dumps(newdd, indent=2)