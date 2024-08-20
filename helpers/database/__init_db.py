import sqlite3
from Globals import DATABASE_NAME
from flask import g

from helpers.logging import logger

def get_db_connection():
    conn = getattr(g, '_database', None)
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        logger.info("Foi feita uma conexão com o banco!")
    except sqlite3.Error as e:
        logger.error(f"Não foi possível conectar 😥 {e}")

    return conn