
import json


class AsueRoute:
    
    def __init__(
        self, 
        path :str,
        instance :object,
        ):
        self.path = path
        self.instance = instance
        
    @classmethod   
    def register_resource(
        cls,
        resources :list, 
        instance :object
        ): 
        resources.append(AsueRoute(
            instance=instance, 
            path=instance.route
        ))    
        
    @classmethod 
    def register(cls, instance :object, resources :list):
        
        cls.register_resource(resources=resources, instance=instance)    
            
    def get_json_route(self):
        return self.__dict__
    
class AsueWebsocket:
    
    def __init__(self, send, receive, scope):
        self._scope = scope
        self._send = send 
        self._receive = receive
        
    async def recv(self):
        order = await self._receive()
        if order['type']=='websocket.connect':
            await self._send({'type': 'websocket.accept'})
            order = await self._receive()
            if order['type']=='websocket.receive':
                return json.loads(order['text'])
            elif order['type']=='websocket.disconnect': 
                await self._send({'type': 'websocket.close'})
    
    async def emit(self, data):
        await self._send({'type': 'websocket.send', 'text': data})