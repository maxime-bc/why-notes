# import psycopg2
# from psycopg2._psycopg import OperationalError
# from psycopg2.extras import DictCursor
# from psycopg2.extensions import connection
#
#
# class Connection(object):
#
#     def __init__(self):
#         self._connection = self._get_connection()
#         self._host = "no-sql-project_postgresql_1"
#         self._user = "docker"
#         self._password = "docker"
#         self._database = "docker"
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self._connection.commit()
#         self._connection.close()
#
#     def __del__(self):
#         # Can fail if connection is already closed thus we get a try
#         try:
#             self._connection.commit()
#             self._connection.close()
#         except sqlite3.Error:
#             pass
#
#         # https://stackoverflow.com/a/1830011/427887
#
#     def _get_connection(self) -> connection:
#         conn = None
#         try:
#             conn = psycopg2.connect(host=self._host,
#                                     dbname=self._database,
#                                     user=self._user,
#                                     password=self._password,
#                                     cursor_factory=DictCursor)
#         except OperationalError as e:
#             print(e)
#         return conn
