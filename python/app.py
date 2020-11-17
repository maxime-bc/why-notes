# import psycopg2
# from flask import Flask
# from psycopg2.extras import DictCursor
#
# app = Flask(__name__)
#
# HOST = "no-sql-project_postgresql_1"
# USER = "docker"
# PASSWORD = "docker"
# DATABASE = "docker"
#
#
# @app.route('/')
# def hello_world():
#     # Test postgresql conn, to move
#     conn = psycopg2.connect(host=HOST, dbname=DATABASE, user=USER, password=PASSWORD, cursor_factory=DictCursor)
#     sql = "SELECT * FROM user_profile;"
#     cur = conn.cursor()
#     cur.execute(sql)
#     print(cur.fetchall())
#
#     return 'Hello, World!'
#
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=80)
