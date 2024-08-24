import os
import psycopg2
from psycopg2.extras import RealDictConnection
from flask import g

from helpers.logging import logger

def get_db_connection():
    conn = getattr(g, '_database', None)
    try:
        conn = psycopg2.connect(
            database=os.environ.get('DATABASE_NAME'),  
            user=os.environ.get('DATABASE_USER'), 
            password=os.environ.get('DATABASE_PASSWORD'),  
            host=os.environ.get('DATABASE_HOST'),
            port=os.environ.get('DATABASE_PORT'),
            # Define o RealDictConnection como padrão para 
            # sempre tratar todos os cursors como dict
            connection_factory=RealDictConnection
        ) 
                        
        logger.info("Foi feita uma conexão com o banco!")
    except psycopg2.Error as e:
        logger.error(f"Não foi possível conectar 😥 {e}")

    return conn