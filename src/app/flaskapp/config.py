import os

class Config(object):
    SECRET_KEY = 'fdgg5f5rt86df4gds74grte64gsdfg' # os.urandom(16)
    DEBUG = True
    UPLOAD_FOLDER = 'uploaded'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    IMAGE_FORMAT = 'JPEG'
    IMAGE_EXTENSION = 'jpg'
    APP_PATH = os.path.abspath(os.path.dirname(__file__))

    @property
    def PASSWORD(self):
        try:
            with open(self.APP_PATH+'/password.txt', 'r') as file:
                return file.read()
        except:
            print("Cannot load password.txt")
            return ''