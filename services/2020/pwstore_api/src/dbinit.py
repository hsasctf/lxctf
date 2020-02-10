import sqlite3
from sys import stderr
from typing import Optional

class QueryExecutionError(Exception):
     def __init__(self, msg: str, base_execption: Exception):
         self.base_execption = base_execption
         super().__init__(msg)

class DBconn:

    conn: sqlite3.Connection = None

    def __init__(self, db_path: str, initfile_path: str):

        if not self.conn:
            self.conn: sqlite3.Connection = sqlite3.connect(db_path)
            cur: sqlite3.Cursor = self.conn.cursor()

            with open(initfile_path, 'r') as initfile:
                cur.executescript(initfile.read())

    def __del__(self):
        if self.conn:
            self.conn.close()

    # todo: make query exec async
    def execute_query(self, query: str) -> sqlite3.Cursor:
        try:
            # context manager creates one transaction per block and ensures rollback if failure
            with self.conn as conn:
                return conn.execute(query)
        except Exception as e:
            print(f'[ERROR] query execution failed: {type(e)}, querystr="{query}"', file=stderr)
            raise QueryExecutionError('query execution failed', e)

    
if __name__ == '__main__':

    from os import path
    BASE_DIR = path.dirname(path.abspath(__file__))
    DB_PATH = path.join(BASE_DIR, 'db.sqlite')
    INITFILE_PATH = path.join(BASE_DIR, 'init.sql')
    db = DBconn(DBPATH, INITFILE_PATH)
