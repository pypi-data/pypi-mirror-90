from ..template.useful import encode_data, decode_data
from ..template import AsueTemplateRender

import json

class AsueRequestResponse:
    def __init__(self, send :callable):
        self._send = send
        
        
    async def send(self, response_json :dict=None, response_html :bytes=None):
        
        if response_json:
            await self._send(self._get_first_json_package(response_json=response_json))
            await self._send(self._get_second_json_package(response_json=response_json)) 
             
        if response_html:
            await self._send(self._get_first_html_package())
            await self._send(self._get_second_html_package(response_html=response_html))
            
        
        
    async def renderize_html_page(self, template_name :str):
        self.str = AsueTemplateRender.get_instance()
        html_page_encoded = self.str.render_template(template_name=template_name)
        await self.send(response_html=html_page_encoded)
        
        
    def _get_first_html_package(self):
        first_package = {}
        first_package.update({'type': 'http.response.start'})
        first_package.update({'status': 200})  
        first_package.update({'headers': [
                [encode_data('content-type'), encode_data('text/html')]
            ]
        })  
        return first_package
    
    
    def _get_second_html_package(self, response_html :bytes):
        second_package = {}  
        second_package.update({'type': 'http.response.body'})  
        second_package.update({'body': response_html})
        return second_package
        
        
    def _get_first_json_package(self, response_json :dict):
        first_package = {}  
        first_package.update({'type': 'http.response.start'})
        if 'status' in response_json:
            first_package.update({'status': response_json['status']})
        else:
            first_package.update({'status': 200})
            
        if 'headers' in response_json:
            headers = [] 
            if 'content-type' in response_json['headers']:
                headers.append([
                    encode_data('content-type'), 
                    encode_data(response_json['headers']['content-type'])
                    ])
            first_package.update({'headers': headers})
        else:
            first_package.update({'headers': [
                [encode_data('content-type'), encode_data('application/json')]
                ]
            })          
        return first_package
    
    
    def _get_second_json_package(self, response_json :dict):
        second_package = {}  
        second_package.update({'type': 'http.response.body'})
        if 'status' in response_json:
            del response_json['status']
        if 'headers' in response_json:
            del response_json['headers']
        second_package.update({'body': encode_data(json.dumps(response_json))})
        return second_package
        
        
        