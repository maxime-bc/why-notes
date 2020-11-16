from flask import Flask
import psycopg2
from psycopg2.extras import DictCursor
app = Flask(__name__)

# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
HOST = "app_postgresql_1"
USER = "docker"
PASSWORD = "docker"
DATABASE = "docker"


@app.route('/')
def hello_world():
    # Open connection
    conn = psycopg2.connect(host=HOST, dbname=DATABASE, user=USER, password=PASSWORD, cursor_factory=DictCursor)

    # Open a cursor to send SQL commands
    cur = conn.cursor()

    #
    # # Execute a SQL INSERT command
    #
    # sql = "INSERT INTO user_profile (email, pwd, first_name, last_name) " \
    #       "VALUES ('test@gmail.com', '1234', 'test', 'test')"
    #
    # cur.execute(sql)
    #
    # # Commit (transactionnal mode is by default)
    #
    # conn.commit()

    # Testing
    sql = "SELECT * FROM user_profile;"




    cur.execute(sql)

    users = cur.fetchall()

    res = ''
    for row in users:
        print(row)
        res += "Id = " + str(row['id'])

    # Close connection

    conn.close()

    return res


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
