import datetime as dt
import psycopg2
import json
import os
from common import superuser_login

from urllib.parse import urljoin
import requests
from config import config
from uploader.parsers.WSConnections import WSConnection

dbname = os.getenv("DB_NAME", "ludhiana_legacy_data")
dbuser = os.getenv("DB_USER", "postgres")
dbpassword = os.getenv("DB_PASSWORD", "postgres")
tenant = os.getenv("TENANT", "pb.ludhiana")
city = os.getenv("CITY", "LUDHIANA")
host = os.getenv("DB_HOST", "localhost")
batch = os.getenv("BATCH_NAME", "2")
table_name = os.getenv("TABLE_NAME", "ludhiana_ws_legacy_data")
default_phone = os.getenv("DEFAULT_PHONE", "9999999999")
default_locality = os.getenv("DEFAULT_LOCALITY", "UNKNOWN")
batch_size = os.getenv("BATCH_SIZE", "100")

dry_run = True

#connection_db_pt = psycopg2.connect("dbname={} user={} password={} host={}".format(dbname, dbuser, dbpassword, host))
connection_db_ws = psycopg2.connect("dbname={} user={} password={} host={}".format(dbname, dbuser, dbpassword, host))
cursor_ws = connection_db_ws.cursor()
#cursor_pt = connection.cursor()
postgresql_select_Query = """
select row_to_json(cd) from {} as cd 
where 
cd.upload_status is NULL and
cd.new_propertyid is not null 
and batchname = '{}' 
limit {} 
""".format(table_name, batch, batch_size)


def update_db_record(uuid, **kwargs):
    columns = []
    for key in kwargs.keys():
        columns.append(key + "=%s")

    query = """UPDATE {} SET {} where uuid = %s""".format(table_name, ",".join(columns))
    cursor_ws.execute(query, list(kwargs.values()) + [uuid])
    connection_db_ws.commit()
    pass


def main():
    continue_processing = True
    access_token = superuser_login()["access_token"]
    import time

    while continue_processing:
        cursor_ws.execute(postgresql_select_Query)
        data = cursor_ws.fetchmany(int(batch_size))

        # continue_processing = False
        if not data:
            print("No more data to process. Script exiting")
            continue_processing = False
            cursor_ws.close()
            connection_db_ws.close()

        for row in data:
            json_data = row[0]
            uuid = json_data["uuid"]
            print('Processing {}'.format(uuid))
            print("property uid")








if __name__ == "__main__":
    main()