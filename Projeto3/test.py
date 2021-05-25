import requests
import sqlite3
import json

def get_db_connection():
    conn = sqlite3.connect('RateAlbums.db')
    return conn

conn = get_db_connection()
query = conn.execute('SELECT * FROM listas_albuns').fetchall()
print(query)

