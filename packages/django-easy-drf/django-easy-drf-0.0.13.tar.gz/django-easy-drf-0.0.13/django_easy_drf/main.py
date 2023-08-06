from .core import Creator, TemplateHandler, FileHandler
from .drf_handlers import SerializersHandler, ViewsHandler, URLsHandler


files_mapping = {
    'v': ViewsHandler,
    's': SerializersHandler,
    'u': URLsHandler
}

def create_all(current_directory, files, force=False):

    if not force:
        response = input("""Warning: the content of serializers.py, views.py and urls.py will be overwritten
Do you want to continue? [Y/n] """)

    if force or response == "" or response == 'y' or response == 'Y':
        creator = get_creator(current_directory, *get_file_handlers(files))

        creator.create()

def get_file_handlers(files):
    return [files_mapping.get(file_key) for file_key in files]

def get_creator(directory, *klasses):
    template_handler = TemplateHandler(FileHandler())

    return Creator(directory, [klass(template_handler) for klass in klasses], template_handler)
