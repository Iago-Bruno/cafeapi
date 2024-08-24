import os
import psycopg2
import sqlite3
from dotenv import load_dotenv

connection = psycopg2.connect(
            database=os.environ.get('DATABASE_NAME'),  
            user=os.environ.get('DATABASE_USER'), 
            password=os.environ.get('DATABASE_PASSWORD'),  
            host=os.environ.get('DATABASE_HOST'),
            port=os.environ.get('DATABASE_PORT')
        ) 

with open('schema.sql') as f:
    cursor = connection.cursor()
    cursor.execute(f.read())
    # connection.executescript(f.read())

connection.commit()
connection.close()
