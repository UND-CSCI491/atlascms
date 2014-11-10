class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI

class ConfigDevelopment(Config):
    '''Used for local development.'''
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI

class ConfigUnitTesting(Config):
    '''Used for unit testing purposes.'''
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = False
    DATABASE_URI = 'sqlite:///unittest.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
