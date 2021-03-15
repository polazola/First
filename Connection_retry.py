import os
import sqlite3
import time

from CustomLogger import logger
from project_exceptions import NoDatabaseError


def connection_retry(func):
    def wrapper( **kwargs):
        tries = kwargs['tries']
        delay = kwargs['delay']
        db_name = kwargs['db_name']
        for i in range(int(tries)):
            logger.info(f"It is my {i+1} try to connect")
            conn = None
            if os.path.isfile(db_name): #tutaj sprawdzenie czy jest taki plik bo wcześniej nam tworzył a tego nie chcemy
                try:
                    conn = sqlite3.connect(db_name, timeout=20)
                except Exception as e:
                    logger.error(f"The {i+1} attempt failed", exc_info=True)
                    time.sleep(delay)
                else:
                    logger.info(f"Connection established")
                return conn
            else:
                logger.error(f"No database {db_name}")


    return wrapper