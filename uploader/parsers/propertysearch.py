import requests
import json
import psycopg2
class propsearch():
    db_config = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'postgres',
        'database': 'ludhiana_legacy_data',
    }

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ludhiana_ws_legacy_data WHERE status != 'sent' OR status IS NULL")
    rec = cursor.fetchall()