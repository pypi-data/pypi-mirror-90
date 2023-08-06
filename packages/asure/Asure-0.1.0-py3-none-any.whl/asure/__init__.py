

from .models.routes import AsureBaseClassRoute
from .models.websocket import AsureBaseWebsocket
from .template import AsueTemplateRender
from .request import AsueRequestObject
from .resource import AsueRoute
from .primitive import Handler

import nest_asyncio
import uvicorn 
import asyncio
import json

nest_asyncio.apply()

h = Handler()

async def server(scope, receive, send):
    if scope['type'] == 'http':
        request = AsueRequestObject(scope=scope, receive=receive, send=send)
        for resource in Asure.get_routes():       
            await h.inject_routes_dependencies(request=request, resource=resource)  
    if scope['type'] == 'websocket' and Asure.has_ws():
        await h.get_ws_connection(scope=scope, receive=receive, send=send, ws_handler=Asure.get_ws())
   
class Asure:
    
    RESOURCES = []
    ws = None
    currently_app = None
    
    def __init__(self, templates_dir :str=None, statics_dir :str=None):
                
        Asure.set_currently_app(app=self)          
        self.atr = AsueTemplateRender()       
        if templates_dir:    
            self.atr.get_directory_templates(templates_dir)
        if statics_dir:
            self.atr.get_directory_statics(statics_dir)
            
    
    @classmethod    
    def set_currently_app(cls, app):
        if cls.currently_app == None:
            cls.currently_app = app
       
        
    @classmethod
    def get_currently_app(cls):
        return cls.currently_app 
        
        
    @classmethod
    def set_ws(cls, ws):
        cls.ws = ws
        
        
    @classmethod
    def get_ws(cls):
        return cls.ws
        
        
    @classmethod
    def has_ws(cls):
        if cls.ws!=None:
            return True 
        else:
            return False
        
        
    @classmethod
    def get_routes(cls):
        return cls.RESOURCES 
     
     
    def add_resource(self, 
        route_class=None,
        route_path :str=None,
        websocket_resource :AsureBaseWebsocket=None):
        
        if route_class and route_path: 
            AsueRoute.register(instance=route_class(route=route_path), resources=Asure.get_routes())
        if websocket_resource: 
            Asure.set_ws(ws=websocket_resource())
                                              
                           
    def run(self, host: str, port: int):  
        uvicorn.run("asure:server", log_level="info", host=host, port=port)