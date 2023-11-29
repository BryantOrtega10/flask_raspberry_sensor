class Config(object):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = True
    SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'

class DevelpmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '5e3d937f09a95865e69e2b91920bf642929bb1edbc45f2fbe38eb57fc037aa56'
