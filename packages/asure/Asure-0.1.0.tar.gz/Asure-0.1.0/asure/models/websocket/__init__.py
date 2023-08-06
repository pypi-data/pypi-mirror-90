from ...resource import AsueWebsocket
from abc import abstractmethod

class AsureBaseWebsocket:
    
    @abstractmethod
    async def handler(self, websocket :AsueWebsocket):
        pass 