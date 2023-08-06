import os
import ast
import astunparse

class Creator:
    def __init__(self, directory, drf_handlers, template_handler):
        self.directory = directory
        self.drf_handlers = drf_handlers
        self.template_handler = template_handler
        
    def create(self):
        model_classes = self.template_handler.get_model_classes(self.directory)

        templates = dict()
        for handler in self.drf_handlers:
            templates[handler.code] = self.template_handler.get_template(handler.code)

        for model_class in model_classes:
            for handler in self.drf_handlers:
                handler.handle(templates.get(handler.code), model_class)

        for handler in self.drf_handlers:
            self.template_handler.write_result(handler.result_name, templates.get(handler.code))


class TemplateHandler:
    def __init__(self, file_handler):
        super().__init__()
        self.file_handler = file_handler
        
    def get_model_classes(self, directory):
        path  = os.path.join(directory, 'models.py')
        models_ast = ast.parse(self.file_handler.read(path))

        return [clss for clss in models_ast.body if clss.__class__ is ast.ClassDef]

    def get_template(self, template_name, **kwargs):
        script_folder = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_folder, f'templates/{template_name}')

        return ast.parse(self.file_handler.read(path, **kwargs))

    def write_result(self, result_file_name, template):
        self.file_handler.write(result_file_name, astunparse.unparse(template))


class FileHandler:
    def read(self, path, **kwargs):
        with open(path, 'r') as file:
            return file.read().format(**kwargs)

    def write(self, path, content):
         with open(path, 'w') as wfile:
            wfile.write(content) 

    