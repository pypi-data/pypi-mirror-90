from ..resource import AsueWebsocket, AsueRoute
from .useful import encode_data, decode_data
from ..request import AsueRequestObject
import asyncio
import json

class Handler:

    async def inject_routes_dependencies(self, request: AsueRequestObject, resource: AsueRoute):    
        
        if request.path==resource.path:      
                     
            if request.method=='VIEW':
                try:                  
                    await resource.instance.view(response=request.responser, request=request)   
                except:
                    raise 'Route is not defined'                
            if request.method=='POST':                   
                await resource.instance.post(response=request.responser, request=request)                  
            if request.method=='GET':                
                await resource.instance.get(response=request.responser, request=request)                
            if request.method=='DELETE':               
                await resource.instance.delete(response=request.responser, request=request)                
            if request.method=='PUT':               
                await resource.instance.put(response=request.responser, request=request)                 
            if request.method=='PATCH':               
                await resource.instance.patch(response=request.responser, request=request)              
                                  
    
    async def get_ws_connection(self, scope, receive, send, ws_handler):
              
        await ws_handler.handler(
            websocket= AsueWebsocket(
                receive=receive,
                scope=scope, 
                send=send
            )
        )


    def to_response(self, send, 
        content_type :str='application/json',                   
        json_response :dict=None, template :bytes=None):
    
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)     
        loop.run_until_complete(self._response(         
            send=send,        
            template=template,       
            json_response=json_response,         
            content_type=content_type         
        ))
        

    async def _response(self, send, content_type :str, template :bytes=None, json_response :dict=None):   
        
        if template:        
            response_data = template        
        elif json_response:      
            response_data = json_response           
        if template==None and json_response==None:   
            raise 'Response no defined'      
         
        if isinstance(response_data, dict):      
            response_data = encode_data(json.dumps(response_data))          
        try:        
            self.send_in_order(function=self.send_first_package(      
                response_data=response_data,
                content_type=content_type,
                send=send
                )
            )                  
        except RuntimeError:      
            pass