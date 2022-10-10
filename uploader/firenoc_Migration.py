import datetime as dt
import psycopg2
import json
import os
from common import superuser_login
from  FireNocApplication import *


from urllib.parse import urljoin
import requests
from config import config
#from uploader.parsers.ikon import IkonProperty
from uploader.parsers.ikonV2 import IkonPropertyV2


dbname = os.getenv("DB_NAME", "firenoc_legacy_data")
dbuser = os.getenv("DB_USER", "postgres")
dbpassword = os.getenv("DB_PASSWORD", "postgres")
tenant = os.getenv("TENANT", "pb.zira")
city = os.getenv("CITY", "ZIRA")
host = os.getenv("DB_HOST", "localhost")
#batch = os.getenv("BATCH_NAME", "2")
table_name = os.getenv("TABLE_NAME", "firenoc_zira_legacy_data")
default_phone = os.getenv("DEFAULT_PHONE", "9999999999")
default_locality = os.getenv("DEFAULT_LOCALITY", "UNKNOWN")
batch_size = os.getenv("BATCH_SIZE", "100")

district="pb.ferozepur"
subdistrict="pb.zira"
firestation_id="FS_ZIRA_01"

#dry_run = (False, True)[os.getenv("DRY_RUN", "True").lower() == "true"]
dry_run = False


connection = psycopg2.connect("dbname={} user={} password={} host={}".format(dbname, dbuser, dbpassword, host))
cursor = connection.cursor()
postgresql_select_Query = """
select row_to_json(pd) from {} as pd 
where 
pd.upload_status is NULL 
limit {} 
""".format(table_name,  batch_size)

continue_processing = True
access_token = superuser_login()["access_token"]
import time

cursor.execute(postgresql_select_Query)
data = cursor.fetchmany(int(batch_size))

continue_processing = False
if not data:
    print("No more data to process. Script exiting")
    continue_processing = False
    cursor.close()
    connection.close()
c=0
for row in data:
    c=c+1
    json_data = row[0]
    uuid = json_data["uuid"]
    print('Processing {} counter {}'.format(uuid,c))
    try:
        application_record=FireNocRecord(json_data)
        application_record.process_record(json_data,district,subdistrict,firestation_id)
        #uploading firenoc application
        start = time.time()
        req, res = application_record.upload_Application(access_token)
        time_taken = time.time() - start
    except Exception as ex:
        print("Exception  Occurred ... ")
        import traceback
        traceback.print_exc()

    if continue_processing == False:
        print("single record checked only")
        exit(0)






