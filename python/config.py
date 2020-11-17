class Config(object):
    HOST = 'no-sql-project_postgresql_1'
    USER = 'docker'
    PASSWORD = 'docker'
    DATABASE = 'docker'
    DIALECT = 'postgresql'
    DRIVER = 'psycopg2'
    SQLALCHEMY_DATABASE_URI = f'{DIALECT}+{DRIVER}://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
