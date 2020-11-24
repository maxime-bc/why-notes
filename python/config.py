class Config(object):
    # flask config 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12345678'

    # postgresql config
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://docker:docker@postgresql/docker'

    # redis config
    REDIS_URL = f'redis://:@redis:6379/0'
