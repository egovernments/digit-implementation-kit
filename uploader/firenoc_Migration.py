import datetime as dt
import psycopg2
import json
import os
from typing import Optional, List
from common import superuser_login
from  FireNocApplication import *


# to Approve PB-FN-2022-10-26-061179


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
# batch = os.getenv("BATCH_NAME", "2")
table_name = os.getenv("TABLE_NAME", "firenoc_zira_legacy_data")
default_phone = os.getenv("DEFAULT_PHONE", "9999999999")
default_locality = os.getenv("DEFAULT_LOCALITY", "UNKNOWN")
batch_size = os.getenv("BATCH_SIZE", "100")

district = "pb.ferozepur"
subdistrict = "pb.zira"
firestation_id = "FS_ZIRA_01"

# dry_run = (False, True)[os.getenv("DRY_RUN", "True").lower() == "true"]
dry_run = False

connection = psycopg2.connect("dbname={} user={} password={} host={}".format(dbname, dbuser, dbpassword, host))
cursor = connection.cursor()
postgresql_select_Query = """
    select row_to_json(pd) from {} as pd 
    where 
    pd.upload_status is NULL 
    limit {} 
    """.format(table_name, batch_size)

continue_processing = True
access_token = superuser_login()["access_token"]
import time


def main():
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
            print(res)
            time_taken = time.time() - start
            if "FireNOCs" in res:
                applicationNumber = res["FireNOCs"][0]["fireNOCDetails"]["applicationNumber"]
                print("Application Number Alloted : ",applicationNumber)
                #updating upload status
                update_db_record(uuid, upload_response=json.dumps(res),upload_request=json.dumps(req),upload_status="COMPLETED",new_application_number=applicationNumber)

                valid_from=int((dt.datetime.strptime(json_data["date_of_approval"],'%Y-%m-%d %H:%M:%S')).timestamp())* 1000 #epoch in milliseconds
                valid_upto=int((dt.datetime.strptime(json_data["noc_valid_upto"],'%Y-%m-%d')).timestamp())* 1000 #epoch in milliseconds

                #updating query 1: update eg_fn_firenocdetail set status='APPROVED', financialyear='2022-23', validfrom=1655444485933, validto=1655444485933,issueddate=1635705000000 where uuid=(select uuid from eg_fn_firenocdetail where applicationNumber='PB-FN-2022-10-11-103285' and status='INITIATED' and tenantid='pb.zira')
                update_db_record_approve_application_query1(uuid, status='APPROVED',financialyear='2021-22',validfrom=valid_from,
                                 validto=valid_upto, issueddate=valid_from, applicationNumber=applicationNumber, tenantid=subdistrict)
                #updating query 2 : update eg_fn_firenoc set firenocnumber='1111-23455-Fire-2222',oldfirenocnumber='123',islegacy=true where uuid=(select firenocuuid from eg_fn_firenocdetail where applicationNumber='PB-FN-2022-10-11-103285'  and tenantid='pb.zira')
                update_db_record_approve_application_query2(uuid,firenocnumber=json_data["new_noc_no"],oldfirenocnumber=json_data["old_noc_no"], applicationNumber=applicationNumber, tenantid=subdistrict)


        except Exception as ex:
            print("Exception  Occurred ... ")
            update_db_record(uuid, upload_response=json.dumps(res), upload_request=json.dumps(req),
                             upload_status="EXCEPTION")
            import traceback
            traceback.print_exc()

        if continue_processing == False:
            print("single record checked only")
            exit(0)



def update_db_record(uuid, **kwargs):
    columns = []
    for key in kwargs.keys():
        columns.append(key + "=%s")

    query = """UPDATE {} SET {} where uuid = %s""".format(table_name, ",".join(columns))
    cursor.execute(query, list(kwargs.values()) + [uuid])
    connection.commit()
    pass


def update_db_record_approve_application_query1(uuid:Optional[str]=None,status:Optional[str]=None, financialyear:Optional[str]=None,validfrom:Optional[str]=None,
                                 validto:Optional[str]=None, issueddate:Optional[str]=None, applicationNumber:Optional[str]=None, tenantid:Optional[str]=None):
    query1="update eg_fn_firenocdetail set status='%s', financialyear='%s', validfrom=%s, validto=%s,issueddate=%s where uuid=(select uuid from eg_fn_firenocdetail where applicationNumber='%s' and status='INITIATED' and tenantid='%s');"%(status,financialyear,validfrom,validto,validfrom,applicationNumber,tenantid)
    update_db_record(uuid, query1=query1)
    pass

def update_db_record_approve_application_query2(uuid,firenocnumber:Optional=None,oldfirenocnumber:Optional=None,applicationNumber:Optional[str]=None, tenantid:Optional[str]=None):
    query2="update eg_fn_firenoc set firenocnumber='%s',oldfirenocnumber='%s' where uuid=(select firenocuuid from eg_fn_firenocdetail where applicationNumber='%s'  and tenantid='%s');"%(firenocnumber,oldfirenocnumber,applicationNumber,tenantid)
    update_db_record(uuid, query2=query2)
    pass

main() #call to main function to start processing