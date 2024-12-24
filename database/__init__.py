import sqlite3 as sql
from .db_utils import *
from .config import DATABASE


def get_connection():
    connection = sql.connect(DATABASE, check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Taxpayers (
        id INTEGER PRIMARY KEY,
        initials TEXT NOT NULL,
        electricity INTEGER,
        cold_water INTEGER,
        hot_water INTEGER,
        gas INTEGER,
        debt REAL,
        payment REAL
        )
        ''')
    connection.commit()
    return connection


def close(connection):
    connection.close()
