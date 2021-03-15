import sqlite3
import os.path #sprawdzamy czy baza istnieje

from Connection_retry import connection_retry
from CustomLogger import logger

from retrying import retry

from project_exceptions import NoDatabaseError

class Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self.connect(tries=3, delay=0.1, db_name=db_name)
        if  self.conn is None:
            raise NoDatabaseError

    @staticmethod
    @connection_retry
    def connect(db_name, *args, **kwargs):
        pass

    def execute_sql(self, sql, params=None):
        if params is None:
            params = []

        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(sql, params)
                self.conn.commit()
            except Exception as e:
                logger.error(f"Can not execute sql: \n{str(sql)}\nError details: {e}")

    def select_all_tasks(self, table_name):
        try:
            #conn = self.connect()
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error(f"Can not fetch database {table_name} data \n" + str(e))

    def close_conn(self):
        try:
            self.conn.close()
        #AttributeError: 'NoneType' object has no attribute 'close'
        except AttributeError as e:
            logger.error(f"Can not close connection because connection was not established:  {e}")


