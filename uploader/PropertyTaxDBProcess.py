import datetime as dt
import psycopg2
import json
import os
from common import superuser_login

from urllib.parse import urljoin
import requests
from config import config
#from uploader.parsers.ikon import IkonProperty
from uploader.parsers.ikonV2 import IkonPropertyV2


dbname = os.getenv("DB_NAME", "muktsar_survey_data")
dbuser = os.getenv("DB_USER", "postgres")
dbpassword = os.getenv("DB_PASSWORD", "postgres")
tenant = os.getenv("TENANT", "pb.muktsar")
city = os.getenv("CITY", "MUKTSAR")
host = os.getenv("DB_HOST", "localhost")
batch = os.getenv("BATCH_NAME", "1")
table_name = os.getenv("TABLE_NAME", "muktsar_pt_survey_data")
default_phone = os.getenv("DEFAULT_PHONE", "9999999999")
default_locality = os.getenv("DEFAULT_LOCALITY", "UNKNOWN")
batch_size = os.getenv("BATCH_SIZE", "100")

#dry_run = (False, True)[os.getenv("DRY_RUN", "True").lower() == "true"]
dry_run = False

connection = psycopg2.connect("dbname={} user={} password={} host={}".format(dbname, dbuser, dbpassword, host))
cursor = connection.cursor()
postgresql_select_Query = """
select row_to_json(pd) from {} as pd 
where 
pd.upload_status is NULL and
pd.new_locality_code is not null 
and batchname = '{}' and propertytype is not null
limit {} 
""".format(table_name, batch, batch_size)


def update_db_record(uuid, **kwargs):
    columns = []
    for key in kwargs.keys():
        columns.append(key + "=%s")

    query = """UPDATE {} SET {} where uuid = %s""".format(table_name, ",".join(columns))
    cursor.execute(query, list(kwargs.values()) + [uuid])
    connection.commit()
    pass


def update_db_record_assessment(pt_uid, **kwargs):
    columns = []
    for key in kwargs.keys():
        columns.append(key + "=%s")

    query = """UPDATE {} SET {} where returnid = concat(%s,'_',acknowledgementno)""".format(table_name, ",".join(columns))
    cursor.execute(query, list(kwargs.values()) + [pt_uid])
    connection.commit()
    pass


def main():
    continue_processing = True
    access_token = superuser_login()["access_token"]
    import time

    while continue_processing:
        cursor.execute(postgresql_select_Query)
        data = cursor.fetchmany(int(batch_size))

        # continue_processing = False
        if not data:
            print("No more data to process. Script exiting")
            continue_processing = False
            cursor.close()
            connection.close()

        for row in data:
            json_data = row[0]
            uuid = json_data["uuid"]
            print('Processing {}'.format(uuid))
            try:
                p = IkonPropertyV2()
                p.process_record(json_data, tenant, city)
                #pd = p.property_details[0]
                #financial_year =  json_data["session"].replace("-20", "-")
                # p.tenant_id = tenant
                # for o in pd.owners:
                #     o.mobile_number = default_phone
                # pd.citizen_info.mobile_number = default_phone
                #p.source = "LEGACY_RECORD"
                # p.address.locality = {
                #     "code": default_locality,
                #     "area": "AREA1"
                # }'landArea' (239735496) = {str} '425 Sq. Yard'
                #p.additional_details = {}

                start = time.time()
                req, res = p.upload_property(access_token)
                time_taken = time.time() - start

                if "Properties" in res:
                    pt_id = res["Properties"][0]["propertyId"]
                    old_property_id= json_data["returnid"]
                    ack_no = res["Properties"][0]["acknowldgementNumber"]
                    #calc = res["Properties"][0]["propertyDetails"][0]["calculation"] #only property created in V2, not assement yet
                    #total_amount = calc["totalAmount"]
                    #tax_amount = calc["taxAmount"]
                    # upload_status = "COMPLETED"
                    print("Record updloaded successfully", pt_id)
                    update_db_record(uuid, upload_status="COMPLETED",
                                     upload_response=json.dumps(res),
                                     #new_tax=tax_amount,
                                     #new_total=total_amount,
                                     new_propertyid=pt_id,
                                     new_assessmentnumber=ack_no,
                                     req_json=json.dumps(req),
                                     time_taken=time_taken)
                    # to Approve property as in V2 newly created property is in INWROFLOW status
                    # search property by acknowledgement number

                    #below loop id used as found property with status 'INWORKFLOW' is not successfully being searched in frequent
                    tryagain = True
                    while tryagain == True:
                         try:
                             request_data = {
                                 "RequestInfo": {
                                            "authToken": access_token
                                        }
                                    }

                             response = requests.post(
                                 urljoin(config.HOST, "/property-services/property/_search?acknowledgementIds="+ack_no+"&tenantId=pb.muktsar"),
                                 json=request_data)

                             res=response.json()

                             property_added=res["Properties"][0]
                             tryagain = False
                         except Exception as ee:
                             print("kafka problem, wait and retry")
                             time.sleep(0.5)
                             continue

                    property_added["0"] = {"comment": "", "assignee": []}
                    property_added["workflow"] = {"id": None, "tenantId": "pb.muktsar", "businessService": "PT.CREATE","businessId": ack_no, "action": "APPROVE", "moduleName": "PT","state": None, "comment": None, "documents": None, "assignes": None}

                    request_data = {
                         "RequestInfo": {
                             "authToken": access_token
                         },

                         "Property": property_added
                     }
                    # print(json.dumps(request_data, indent=2))
                    response = requests.post(
                         urljoin(config.HOST, "/property-services/property/_update?tenantId="),
                         json=request_data)

                    res = response.json()
                    update_db_record(uuid, upload_response_workflow=json.dumps(res))  #storing response updating property status as ACTIVATE to approve property
                    print("APPROVED", pt_id)
                    #
                    # # to create assessment(s)
                    #
                    # connection2 = psycopg2.connect(
                    #     "dbname={} user={} password={} host={}".format(dbname, dbuser, dbpassword, host))
                    # cursor2 = connection.cursor()
                    # postgresql_select_Query2 = """
                    # select row_to_json(pd) from {} as pd
                    # where
                    # returnid like '{}' and
                    # pd.new_locality_code is not null and (chequestatus is null or chequestatus!='Bounced')
                    # """.format(table_name, old_property_id)
                    #
                    # cursor2.execute(postgresql_select_Query2)
                    # data2 = cursor2.fetchmany(int(batch_size))
                    # for row2 in data2:
                    #     json_data2 = row2[0]
                    #     fy=json_data2["session"].replace("-20", "-")
                    #     try:
                    #         assessmentDate=dt.datetime.strptime(json_data2["paymentdate"], "%d-%m-%Y").strftime('%Y-%m-%d')
                    #         assessmentTime=time.strptime(assessmentDate,'%Y-%m-%d')
                    #         assementEpoch=time.mktime(assessmentTime)*1000
                    #     except Exception as eex:
                    #         #continue  # skip this assessment as in mohali paymentdate or paymentmode NULL means only estimate was given
                    #         assementEpoch = 946665000000 # 01-Jan-2000 default assessment epoch time
                    #     request_data={"RequestInfo": {"apiId": "Rainmaker", "ver": ".01", "ts": "", "action": "_create", "did": "1",
                    #               "key": "", "msgId": "20170310130900|en_IN",
                    #               "authToken": access_token
                    #                               },
                    #               "Assessment": {"tenantId": "pb.patiala", "propertyId": pt_id,
                    #               #"financialYear": fy, "assessmentDate": time.time(),
                    #               "financialYear": fy, "assessmentDate": assementEpoch,
                    #               "source": "LEGACY_RECORD", "channel": "LEGACY_MIGRATION", "additionalDetails": {}}}
                    #     response = requests.post(
                    #     urljoin(config.HOST, "/property-services/assessment/_create?tenantId=pb.patiala"),
                    #     json=request_data)
                    #     res = response.json()
                    #     update_db_record_assessment(old_property_id, upload_response_assessment=json.dumps(res))  # creating assessment and storeing the response
                    #     print("Assessment Created", pt_id,"  ",fy)

                else:
                    # Some error has occurred
                    print("Error occured while uploading data")
                    print(json.dumps(req, indent=1))
                    print(json.dumps(res, indent=1))
                    update_db_record(uuid, upload_status="ERROR",
                                     upload_response=json.dumps(res),
                                     req_json=json.dumps(req))
            except Exception as ex:
                import traceback
                traceback.print_exc()
                update_db_record(uuid, upload_status="EXCEPTION", upload_response=str(ex))

            if dry_run:
                print("Dry run only, exiting now")
                exit(0)


if __name__ == "__main__":
    main()
