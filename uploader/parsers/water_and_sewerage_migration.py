from common import *
from config.dbfile import *
import requests
from uploader.parsers.water import WaterConnection
from uploader.parsers.sewerage import SewerageConnection


postgresql_select_Query = """
select row_to_json(cd) from {} as cd 
where 
((cd.water_upload_status is null or cd.water_upload_status='ERROR') or (cd.sewerage_upload_status is null OR cd.sewerage_upload_status='ERROR') )
and
cd.new_propertyid is not  NULL
and (cd.isconmig is null or cd.isconmig='False')
and batchname = '{}'
limit 100
""".format(table_name, batch)



def main():
    continue_processing = True
    dry_run=True # only one record to migrate
    access_token = superuser_login()["access_token"]
    while continue_processing:
        print(postgresql_select_Query)
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
            connectionumber=json_data["pkwsid"]
            print('Processing {}'.format(uuid))
            iswater=json_data["water_upload_status"]
            issewerage=json_data["sewerage_upload_status"]
            propertyid = json_data["new_propertyid"]
            print("Searching Property In Digit " + str(propertyid))
            print("Migrating Connection Number "+ connectionumber)
            url = implementation_url+"property-services/property/_search?tenantId=" + tenant + "&propertyIds=" + propertyid + ""
            request_body = {
                'RequestInfo': {
                    'apiId': 'Mihy',
                    'ver': '.01',
                    'action': '',
                    'did': '1',
                    'key': '',
                    'msgId': '20170310130900|en_IN',
                    'requesterId': '',
                    "authToken": access_token
                    }
                }
            property = requests.post(url, json=request_body)
            property_data = property.json()
            property_response= property_data.get("Properties", {})
            type=json_data["conn_type"]
            if type=="B":
                print("Connection Is of Both Type")
                if iswater!='COMPLETED':
                    WaterConnection(property_response, json_data)
                if issewerage!='COMPLETED':
                    SewerageConnection(property_response, json_data)
            elif type=="W":
                if iswater !='COMPLETED':
                    print("Connection Is of Water Type")
                    WaterConnection(property_response, json_data)

            elif type == "S":
                if issewerage !='COMPLETED':
                    print("Connection Is of Sewerage Type")
                    SewerageConnection(property_response, json_data)

            conn_query = "Select row_to_json(cd) from ludhiana_ws_legacy_data as cd where pkwsid='" + connectionumber + "'"
            cursor_ws.execute(conn_query)
            data = cursor_ws.fetchmany()
            for row in data:
                json_data = row[0]
                iswater = json_data["water_upload_status"]
                issewerage =json_data["sewerage_upload_status"]
            if (type == "B" and iswater == "COMPLETED" and issewerage=="COMPLETED"):
                update_query_seweragetable = "UPDATE ludhiana_ws_legacy_data SET isconmig='True' WHERE pkwsid='" + connectionumber + "';"
                print("Migrated Successfully of Connection Type " + type + " Having  Consumer Code " + connectionumber)
                cursor_ws.execute(update_query_seweragetable)
                connection_db_ws.commit()
            elif (type == "W" and  iswater == "COMPLETED" ):
                update_query_seweragetable = "UPDATE ludhiana_ws_legacy_data SET isconmig='True' WHERE pkwsid='" + connectionumber + "';"
                cursor_ws.execute(update_query_seweragetable)
                connection_db_ws.commit()
                print("Migrated Successfully of Connection Type " + type + " Having  Consumer Code " + connectionumber)
            elif (type == "S" and issewerage=="COMPLETED" ):
                update_query_seweragetable = "UPDATE ludhiana_ws_legacy_data SET isconmig='True' WHERE pkwsid='" + connectionumber + "';"
                cursor_ws.execute(update_query_seweragetable)
                connection_db_ws.commit()
                print("Migrated Successfully of Connection Type " + type + " Having  Consumer Code " + connectionumber)

            if dry_run:
                print("dry run allowed single record processing")
                continue_processing=False
                break


if __name__ == "__main__":
    main()

