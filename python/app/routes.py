import psycopg2
from psycopg2.extras import DictCursor

from app import app


@app.route('/')
@app.route('/index')
def index():
    HOST = 'no-sql-project_postgresql_1'
    USER = 'docker'
    PASSWORD = 'docker'
    DATABASE = 'docker'
    # Test postgresql conn, to move
    conn = psycopg2.connect(host=HOST, dbname=DATABASE, user=USER, password=PASSWORD, cursor_factory=DictCursor)
    sql = "SELECT * FROM pg_tables;"
    cur = conn.cursor()
    cur.execute(sql)
    print(cur.fetchall())

    return "Hello, World!"