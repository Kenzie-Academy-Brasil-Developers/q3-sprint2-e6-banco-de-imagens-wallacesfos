import os
import dotenv

dotenv.load_dotenv()

ALLOWED_EXTENSIONS = str(os.environ.get('ALLOWED_EXTENSIONS'))
FILES_DIRECTORY = str(os.environ.get('FILES_DIRECTORY'))
MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH')

EXTENSIONS_LIST = ALLOWED_EXTENSIONS.split(',')

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)
    for i in EXTENSIONS_LIST:
        os.mkdir(f'{FILES_DIRECTORY}/{i}')