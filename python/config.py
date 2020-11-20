class Config(object):
    _project_name = 'no-sql-project'
    _postgresql_host = _project_name + '_postgresql_1'
    _redis_host = _project_name + '_redis_1'

    # flask config 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '12345678'

    # postgresql config
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://docker:docker@{_postgresql_host}/docker'

    # redis config
    REDIS_URL = f'redis://:@{_redis_host}:6379/0'
