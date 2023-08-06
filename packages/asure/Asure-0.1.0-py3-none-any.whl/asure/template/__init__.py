from .useful import encode_data, decode_data
from string import Template
import os

class AsueTemplateRender:
    
    instance = None
    totaly_files_dir = {}
    
    def __init__(self):
        AsueTemplateRender.set_instance(instance=self)
    
    
    @classmethod
    def set_instance(cls, instance):
        if cls.instance == None:
            cls.instance = instance
        
    
    @classmethod
    def get_instance(cls):
        if cls.instance != None:
            return cls.instance
    
        
    def get_file_dir(self, line :str):
        file_link = line.split('*')[1]
        file_dir = file_link.split('"')[-2]
        file_name = file_dir.split('/')[-1]
        totaly_files_dir = AsueTemplateRender.get_totaly_files_dir()
        for item in totaly_files_dir.items():
            for _dir in item[1]:
                if file_name in _dir:
                    return _dir
    
    def open_file(self, file_dir :str):
        with open(file_dir, 'r') as static_file:
            static_file_list = []
            for line in static_file.readlines():
                static_file_list.append(line)
            return static_file_list

    def check_break_line(self, line :str):
        if '\n' in line:
            return line 
        else:
            return line + '\n'
    
    def replace_style(self, line :str, file_list :list):       
        style_init_structure = '<style type="text/css">\n'
        style_end_structure = '</style>\n'       
        style_structure = []    
        style_structure.append(style_init_structure)
        for lin in file_list:
            style_structure.append(self.check_break_line(line=lin))        
        style_structure.append(style_end_structure)
        style = ''
        for i in style_structure:
            style = style + i          
        return style
    
    def replace_script(self, line :str, file_list :list):
        script_init_structure = '<script type="text/javascript">\n'
        script_end_structure = '</script>\n'  
        script_structure = []
        script_structure.append(script_init_structure)
        for lin in file_list:
            script_structure.append(self.check_break_line(line=lin))
        script_structure.append(script_end_structure)
        script = ''
        for i in script_structure:
            script = script + i 
        return script
    
    
    def insert_static_files(self, line :str, template :list):     
        if 'style(*' in line and '*)' in line:
            css_file_dir =  self.get_file_dir(line=line)
            css_file_list = self.open_file(css_file_dir)
            css_structure = self.replace_style(line=line, file_list=css_file_list)
            return css_structure    
        if 'script(*' in line and '*)' in line:
            js_file_dir = self.get_file_dir(line=line)
            js_file_list = self.open_file(js_file_dir)
            js_structure = self.replace_script(line=line, file_list=js_file_list)
            return js_structure        
        return line
    
    
    @classmethod
    def set_file_dir(cls, key :str, value :list):
        cls.totaly_files_dir.update({key: value})
        
    
    @classmethod
    def get_totaly_files_dir(cls):
        return cls.totaly_files_dir
    
    
    def get_directory_templates(self, template_dir :str):
        html_files_dir = []
        for root, subfolder, filename in os.walk(template_dir):
            for filen in filename:
                if '.html' in filen:
                    html_files_dir.append(os.path.join(root, filen)) 
                    
        AsueTemplateRender.set_file_dir(key='html_files_dir', value=html_files_dir)
    
    def get_css_files_dir(self, static_dir :str):
        css_files_dir = []
        for root, subfolder, filename in os.walk(static_dir):
            for filen in filename:
                if '.css' in filen:
                    css_files_dir.append(os.path.join(root, filen))
        
        AsueTemplateRender.set_file_dir(key='css_files_dir', value=css_files_dir)
                      
                    
    def get_js_files_dir(self, static_dir :str):
        js_files_dir = []
        for root, subfolder, filename in os.walk(static_dir):
            for filen in filename:
                if '.js' in filen:
                    js_files_dir.append(os.path.join(root, filen)) 
                    
        AsueTemplateRender.set_file_dir(key='js_files_dir', value=js_files_dir)    
    
    
    def get_directory_statics(self, static_dir :str):
        self.get_css_files_dir(static_dir=static_dir)  
        self.get_js_files_dir(static_dir=static_dir)
        
        
    def _read_template(self, template_name: str):
        totaly_files_dir = AsueTemplateRender.get_totaly_files_dir()
        for html_template_dir in totaly_files_dir['html_files_dir']:
            if template_name in html_template_dir:          
                with open('./'+html_template_dir, 'r') as template:             
                    nTemplate = [] 
                    for line in template.readlines():
                        nTemplate.append(line)                      
                    page = ''
                    for line in nTemplate:                  
                        page = page + self.insert_static_files(line=line, template=nTemplate) 
                                      
                    return encode_data(page) 
        
        
    def _read_and_insert_datas_into_template(self, template_path :str, context_datas :dict=None):
        if not isinstance(context_datas, dict):
            print('Valor setado em "context_datas" não é do tipo "dict"')
        if not isinstance(template_path, str):
            print('Valor setado em "template_path" não é do tipo "str"')     
        try:        
            with open(f"{self.templates_directory}{template_path}", 'r') as template:              
                new_template = [] 
                for line in template.readlines():
                    new_template.append(line)               
                ste = SpartacusTemplateEngine()
                ste.insert(template_block_total=new_template, context_datas=context_datas)               
                page = ''
                for line in new_template:
                    page = page + line
                return encode_data(page) 
        except FileNotFoundError:
            raise 'Template Not found'


    def render_template(self, template_name, context_datas :dict=None):     
        if context_datas!=None:                
            return self._read_and_insert_datas_into_template(
                context_datas=context_datas, 
                template_path=template
            )                 
        else:                     
            return self._read_template(
                template_name=template_name
            )