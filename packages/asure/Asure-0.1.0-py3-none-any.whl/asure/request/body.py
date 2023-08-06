
from .useful import recoverage

class AsueRequestBody:
    
    def __init__(self, body: dict):
        if isinstance(body, dict):
            for k in body.items():
                key = recoverage(k[0])
                self.__setattr__(key, k[1])
                
                
    def get_json(self):
        return self.__dict__