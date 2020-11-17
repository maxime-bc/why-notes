class Config(object):
    _host = 'no-sql-project_postgresql_1'
    _user = 'docker'
    _password = 'docker'
    _database = 'docker'
    _dialect = 'postgresql'
    _driver = 'psycopg2'
    SQLALCHEMY_DATABASE_URI = f'{_dialect}+{_driver}://{_user}:{_password}@{_host}/{_database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
