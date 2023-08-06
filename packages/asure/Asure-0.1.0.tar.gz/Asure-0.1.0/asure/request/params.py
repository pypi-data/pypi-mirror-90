
from .useful import recoverage

class AsueRequestParams:
    
    def __init__(self, params: dict):
        if isinstance(params, dict):
            for k in params.items():
                key = recoverage(k[0])
                self.__setattr__(key, k[1])
                
    def get_json(self):
        return self.__dict__