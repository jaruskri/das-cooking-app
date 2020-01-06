import os

class Config(object):
    SECRET_KEY = 'fdgg5f5rt86df4gds74grte64gsdfg' # os.urandom(16)
    DEBUG = True
    UPLOAD_FOLDER = 'uploaded'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    IMAGE_FORMAT = 'JPEG'
    IMAGE_EXTENSION = 'jpg'
    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    NUM_RECOMMENDED_RECIPES = 15
    NUM_AVAILABLE_CATEGORIES = 40
    RECIPES_ORDER_CRITERION = "(CAST(shoda AS DOUBLE PRECISION)/pocet_ingredienci*CAST(shoda AS DOUBLE PRECISION)/zvoleno_ingredienci)"
    CLASSIFICATION_THRESHOLD = 0.000

    @property
    def PASSWORD(self):
        try:
            with open(self.APP_PATH+'/password.txt', 'r') as file:
                return file.read()
        except:
            print("Cannot load password.txt")
            return ''

# in separate file
class DbConfig(object):
    DB_USER = ""
    DB_PASSOWRD = ""
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"
    DB_NAME = "cookingapp"