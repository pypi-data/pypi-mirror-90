from ..template.useful import decode_data, encode_data
from .useful import recoverage

class AsueRequestHeaders:
    
    def __init__(self, headers: dict):
        if isinstance(headers, dict):
            for k in headers.items(): 
                key = recoverage(k[0])
                self.__setattr__(key, k[1])
                                       
    def get_json(self):
        return self.__dict__