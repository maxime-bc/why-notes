import psycopg2
from psycopg2.extras import DictCursor

from app import app, db, User, Note


@app.route('/')
@app.route('/index')
def index():
    admin = User(first_name='John', last_name='Doe', email='john.doe@example.com', pwd='123456')
    guest = User(first_name='Johnny', last_name='Doey', email='johnny.doe@example.com', pwd='654321')
    note = Note(title='Test', content='This is a test', author=admin, is_public=False, uuid='1234')
    db.session.add(admin)
    db.session.add(note)
    db.session.add(guest)
    db.session.commit()
    users = User.query.all()
    print(users)
    print(admin.notes.all())

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