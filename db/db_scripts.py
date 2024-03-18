import sqlite3
from dotenv import load_dotenv
import os 
from pprint import pprint
load_dotenv()
DATABASE = os.getenv('DATABASE')
db_name = DATABASE
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    open()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    close()
    return data

# pprint(do('SELECT * FROM Users'))
