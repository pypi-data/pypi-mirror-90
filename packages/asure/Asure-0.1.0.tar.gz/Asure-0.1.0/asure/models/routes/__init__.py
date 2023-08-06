from abc import abstractmethod
from ...request import AsueRequestObject
from ...request.response import AsueRequestResponse


class AsureBaseClassRoute:
  
    def __init__(self, route :str):
        self.route = route
        
    
    @abstractmethod
    async def view(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass
    
    @abstractmethod
    async def get(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass 
    
    @abstractmethod
    async def post(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass
    
    @abstractmethod
    async def put(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass 
    
    @abstractmethod
    async def delete(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass
    
    @abstractmethod
    async def patch(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass
    
    @abstractmethod
    async def head(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass
    
    @abstractmethod
    async def trace(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass
    
    @abstractmethod
    async def connect(self, response :AsueRequestResponse, request :AsueRequestObject):
        pass