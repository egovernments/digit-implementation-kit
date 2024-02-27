from common import *
import requests
from config.dbfile import *
import math
from datetime import datetime
class waterdemand:
    def __init__(self, response,waterData):
        self.response = response
        self.waterData = waterData
        self.demandforwater(self,waterData)

    def demandforwater(self,responses,waterData):

        consumercode =self.waterData['id_no']
        print("Creating Demand For water Connection: " +consumercode)
        taxperiodfrom= str('1680307200000')
        taxperiodto=str('1711909799000')
        old_taxperiodfrom = str('1648771200000')
        old_taxperiodto = str('1680287399000')

        selectquery="Select  row_to_json(cd) from ludhiana_demand as cd where cd.id_no='"+consumercode+"'"
        cursor_ws.execute(selectquery)
        data = cursor_ws.fetchmany()
        if data:
            for row in data:
                json_data = row[0]
                water_current = json_data["water_current"]
                isdemanduploaded = json_data["iswaterdemanduploaded"]
                connno=json_data["id_no"]
                water_arrear_old=float(json_data["water_arrear"])
                water_interest_old = float(json_data["water_interest_arrear"])
                payer = self.response['WaterConnection'][0]['connectionHolders'][0]['uuid']

                water_arrear = math.floor(water_arrear_old)
                water_arrear_decimal = water_arrear_old - water_arrear

                water_interest = math.floor(water_interest_old)
                water_interest_decimal = water_interest_old - water_interest

                total_round=water_arrear_decimal+water_interest_decimal

                total_round_add = math.floor(total_round)
                total_addition = total_round - total_round_add
                if total_round_add>0:
                    water_arrear=water_arrear+total_round_add
                else:
                    water_arrear = water_arrear
                if total_addition>=0.5:
                    round_off="+"+str(round(total_addition, 2))
                else:
                    round_off = "-" + str(round(total_addition, 2))

                old_demand_query="Select  row_to_json(cd) from ludhiana_split_receipt as cd where cd.id_no='"+connno+"'"
                cursor_ws.execute(old_demand_query)
                old_data = cursor_ws.fetchmany()

                total_amount_data=0
                if data:
                    if old_data:
                        for rows in old_data:
                            json_data = rows[0]
                            amountpaid = int(json_data["current_water_paid"])
                            sewerage_arrears = int(water_arrear)
                            total_amount_data = sewerage_arrears + amountpaid
                    else:
                        total_amount_data = water_arrear
                old_due = total_amount_data + float(round_off) + water_interest_old
                print("arrear Water amount "+str(total_amount_data))
                print("Current Water amount " + water_current)
                WS_CHARGE_NEW = {
                    "isPaymentCompleted": False,
                    "id": None,
                    "tenantId": self.response['WaterConnection'][0]['tenantId'],
                    "consumerCode": self.response['WaterConnection'][0]['connectionNo'],
                    "consumerType": "waterConnection",
                    "businessService": "WS",
                    "payer": {
                        "id": None,
                        "userName": self.response['WaterConnection'][0]['connectionHolders'][0]['userName'],
                        "name": self.response['WaterConnection'][0]['connectionHolders'][0]['name'],
                        "type": "CITIZEN",
                        "mobileNumber": self.response['WaterConnection'][0]['connectionHolders'][0]['mobileNumber'],
                        "emailId": None,
                        "roles": [
                            {
                                "id": None,
                                "name": "Citizen",
                                "code": "CITIZEN",
                                "tenantId": "pb"
                            }
                        ],
                        "tenantId": "pb",
                        "uuid": payer
                    },
                    "taxPeriodFrom": taxperiodfrom,
                    "taxPeriodTo": taxperiodto,
                    "demandDetails": [
                        {
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "WS_CHARGE",
                            "taxAmount": water_current,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['WaterConnection'][0]['tenantId']
                        }

                    ],
                    "auditDetails": None,
                    "billExpiryTime": 2592000000,
                    "additionalDetails": None,
                    "minimumAmountPayable": water_current,
                    "status": "ACTIVE"
                }
                old_demand={
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "WS_CHARGE",
                            "taxAmount": total_amount_data,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['WaterConnection'][0]['tenantId']
                        }
                old_interest={
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "WS_TIME_INTEREST",
                            "taxAmount": water_interest,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['WaterConnection'][0]['tenantId']
                        }
                old_roundoff= {
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "WS_Round_Off",
                            "taxAmount": round_off,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['WaterConnection'][0]['tenantId']
                        }


                WS_CHARGE_old = {
                    "isPaymentCompleted": False,
                    "id": None,
                    "tenantId": self.response['WaterConnection'][0]['tenantId'],
                    "consumerCode": self.response['WaterConnection'][0]['connectionNo'],
                    "consumerType": "waterConnection",
                    "businessService": "WS",
                    "payer": {
                        "id": None,
                        "userName": self.response['WaterConnection'][0]['connectionHolders'][0]['userName'],
                        "name": self.response['WaterConnection'][0]['connectionHolders'][0]['name'],
                        "type": "CITIZEN",
                        "mobileNumber": self.response['WaterConnection'][0]['connectionHolders'][0]['mobileNumber'],
                        "emailId": None,
                        "roles": [
                            {
                                "id": None,
                                "name": "Citizen",
                                "code": "CITIZEN",
                                "tenantId": "pb"
                            }
                        ],
                        "tenantId": "pb",
                        "uuid": payer
                    },
                    "taxPeriodFrom": old_taxperiodfrom,
                    "taxPeriodTo": old_taxperiodto,
                    "demandDetails": [old_demand,old_interest,old_roundoff],
                    "auditDetails": None,
                    "billExpiryTime": 2592000000,
                    "additionalDetails": None,
                    "minimumAmountPayable": old_due,
                    "status": "ACTIVE"
                }

                url = implementation_url+"billing-service/demand/_create"
                headers = {
                    "Content-Type": "application/json",
                }
                access_token = superuser_login()["access_token"]
                request_body = {
                    "RequestInfo": {
                        "apiId": "Rainmaker",
                        "ver": "abc",
                        "ts": None,
                        "action": "_jobscheduler",
                        "did": "1",
                        "key": "0107000078",
                        "msgId": "pb.amritsar",
                        "authToken": access_token,
                        "correlationId": None,
                        "userInfo": {
                            "id": 1129330,
                            "userName": "30048|1kLQtFI+5IIm6SFcjIfhZ0tP0zMutTQ=",
                            "name": "30048|xmnsjn0chhlSQakCdJnN1JDAsabIObUqPfdgESHoCA==",
                            "type": "SYSTEM",
                            "mobileNumber": "30048|rCGmyyFAn0sZH/QG9YS9JwjDyvkGl40MWUE=",
                            "emailId": None,
                            "roles": [
                                {
                                    "id": None,
                                    "name": "Employee",
                                    "code": "EMPLOYEE",
                                    "tenantId": "pb"
                                },
                                {
                                    "id": None,
                                    "name": "SYSTEM user for cron job",
                                    "code": "SYSTEM",
                                    "tenantId": "pb"
                                }
                            ],
                            "tenantId": "pb.amritsar",
                            "uuid": "cdbba3bc-5d4f-4742-bbb7-418d8dfce7fd"
                        }
                    },
                    "Demands": [WS_CHARGE_NEW,WS_CHARGE_old]
                }
                request_body_string = json.dumps(request_body)

            if isdemanduploaded=='False':
                demand_response = requests.post(url, headers=headers, data=json.dumps(request_body))
                request=json.dumps(request_body)

                response_decoded = demand_response.content.decode('utf-8')
                response_decoded = json.dumps(response_decoded, indent=2)
                if demand_response.status_code==201:

                    print("Response Code is 200(New Deamand Created) of connection No "+connno)
                    update_query = "UPDATE ludhiana_demand SET water_upload_status='COMPLETED', upload_water_req='"+request_body_string+"', upload_water_response='"+ response_decoded+"', iswaterdemanduploaded='True' WHERE id_no='"+str(connno)+"';"
                    update_query_watertable = "UPDATE ludhiana_ws_legacy_data SET iswaterdemandmigrated='True' WHERE pkwsid='"+str(connno)+"';"
                    cursor_ws.execute(update_query, (request_body_string, response_decoded, str(connno)))
                    cursor_ws.execute(update_query_watertable, (str(connno)))
                    connection_db_ws.commit()
                    fetchbill(connno)
                elif demand_response.status_code==400:
                    print(" Water Demand is already present for given connection "+connno)

                    update_query = "UPDATE ludhiana_demand SET water_upload_status='COMPLETED', upload_water_req='" + request_body_string + "', upload_water_response='" + response_decoded + "', iswaterdemanduploaded='True' WHERE id_no='" + str(
                        connno) + "';"
                    update_query_watertable = "UPDATE ludhiana_ws_legacy_data SET iswaterdemandmigrated='True' WHERE pkwsid='" + str(
                        connno) + "';"
                    cursor_ws.execute(update_query, (request_body_string, response_decoded, str(connno)))
                    cursor_ws.execute(update_query_watertable, (str(connno)))
                    connection_db_ws.commit()
                    fetchbill(connno)
                else:
                    print("ERROR while Demand Generation with error code : "+ demand_response.status_code)
                    update_querys ="UPDATE ludhiana_demand SET  water_upload_status='ERROR',upload_water_req = '"+request_body_string+"',isdemanduploaded='False' WHERE id_no ='"+str(connno)+"'; "
                    cursor_ws.execute(update_querys)
                connection_db_ws.commit()




class fetchbill:
    def __init__(self,response):
        self.response = response
        self.fetchbill(self)

    def fetchbill(self, responses):
        print("Going To fetch the bill for the particular Connection")
        url = implementation_url+"billing-service/bill/v2/_fetchbill?tenantId="+tenant+"&consumerCode="+self.response+"&businessService=WS"
        headers = {
            "Content-Type": "application/json",
        }
        access_token = superuser_login()["access_token"]
        request_body = {
            "RequestInfo": {
                "apiId": "Rainmaker",
                "ver": "abc",
                "ts": None,
                "action": "_jobscheduler",
                "did": "1",
                "key": "0107000078",
                "msgId": "pb.amritsar",
                "authToken": access_token,
                "correlationId": None,
                "userInfo": {
                    "id": 1129330,
                    "userName": "30048|1kLQtFI+5IIm6SFcjIfhZ0tP0zMutTQ=",
                    "name": "30048|xmnsjn0chhlSQakCdJnN1JDAsabIObUqPfdgESHoCA==",
                    "type": "SYSTEM",
                    "mobileNumber": "30048|rCGmyyFAn0sZH/QG9YS9JwjDyvkGl40MWUE=",
                    "emailId": None,
                    "roles": [
                        {
                            "id": None,
                            "name": "Employee",
                            "code": "EMPLOYEE",
                            "tenantId": "pb"
                        },
                        {
                            "id": None,
                            "name": "SYSTEM user for cron job",
                            "code": "SYSTEM",
                            "tenantId": "pb"
                        }
                    ],
                    "tenantId": "pb.amritsar",
                    "uuid": "cdbba3bc-5d4f-4742-bbb7-418d8dfce7fd"
                }
            }
        }

        demand_response = requests.post(url, headers=headers, data=json.dumps(request_body))
        json_data = demand_response.json()

        # Check if "Bill" array has data
        if json_data["Bill"]:
            parsed_json = demand_response.json()
            bill_id = parsed_json["Bill"][0]["id"]
            amount = parsed_json["Bill"][0]["totalAmount"]
            print("Bill Id for this   Particular Water Demand Is: "+bill_id)
            print("Total Water Demand Amount: "+str(amount))
            print("Going To Generate The receipt Of the Particular Water connection No: "+ self.response)
            recepitgeneration(bill_id,amount,self.response)
        else:
            print("Error While fetching the Bill of connection number: "+self.response)

class recepitgeneration:
    def __init__(self,billid,totalamount,connno):
        self.billid = billid
        self.totalamount = totalamount
        self.connno = connno
        self.receiptgenerator(self)

    def receiptgenerator(self, responses):
       # print("Going To Generate the receipt for the particular Connection")
        url = implementation_url+"collection-services/payments/_create?"
        headers = {
            "Content-Type": "application/json",
        }
        access_token = superuser_login()["access_token"]
        receipt_query = "Select  row_to_json(cd) from ludhiana_split_receipt as cd where cd.id_no='" + self.connno + "'"
        cursor_ws.execute(receipt_query)
        data = cursor_ws.fetchmany()
        for rows in data:
            json_data = rows[0]
            current_arrear_water_paid = int(json_data["current_arrear_water_paid"])
            current_arrear_water_interest_paid = int(json_data["current_arrear_int_water_paid"])
            current_water_paid = int(json_data["current_water_paid"])
            total_amount=current_arrear_water_paid+current_arrear_water_interest_paid+current_water_paid
            reciept_book_no = json_data["g8_book_no"]
            reciept_date= json_data["payment_date"]
            date_format = '%d-%m-%Y'
            date_object = datetime.strptime(reciept_date, date_format)
            epoch_timestamp = int(date_object.timestamp())
            receipt_no = json_data["g8_receipt_no"]
            transactionNumber=json_data["transaction_id"]
            paymentmode =json_data["payment_mode"]
            iswaterrecepituploaded = json_data["isreceiptwatermigrated"]
            if receipt_no!=None and reciept_book_no!=None:
                reciept_book_no = reciept_book_no + "/" + receipt_no
                payment={
                    "manualReceiptDate": epoch_timestamp,
                    "manualReceiptNumber": reciept_book_no,
                    "businessService": "WS",
                    "billId": self.billid,
                    "totalDue": self.totalamount,
                    "totalAmountPaid": total_amount
                         }

            else:
                payment={
                    "businessService": "WS",
                    "billId": self.billid,
                    "totalDue": self.totalamount,
                    "totalAmountPaid": total_amount
                }
        owner_query = "Select  row_to_json(cd) from ludhiana_ws_legacy_data as cd where cd.pkwsid='" + self.connno + "'"
        cursor_ws.execute(owner_query)
        ownerdata = cursor_ws.fetchmany()
        for row in ownerdata:
            json_data = row[0]
            ownerdata = json_data["ownername"]
            mobile=json_data["mobile"]
            ownerdata = ownerdata
        if data:
            request_body = {
            "RequestInfo": {
                "apiId": "Rainmaker",
                "ver": "abc",
                "ts": None,
                "action": "_jobscheduler",
                "did": "1",
                "key": "",
                "msgId": "",
                "authToken": access_token,
                "correlationId": None,
                "userInfo": {
                    "id": 1129330,
                    "userName": "30048|1kLQtFI+5IIm6SFcjIfhZ0tP0zMutTQ=",
                    "name": "30048|xmnsjn0chhlSQakCdJnN1JDAsabIObUqPfdgESHoCA==",
                    "type": "SYSTEM",
                    "mobileNumber": "30048|rCGmyyFAn0sZH/QG9YS9JwjDyvkGl40MWUE=",
                    "emailId": None,
                    "roles": [
                        {
                            "id": None,
                            "name": "Employee",
                            "code": "EMPLOYEE",
                            "tenantId": "pb"
                        },
                        {
                            "id": None,
                            "name": "SYSTEM user for cron job",
                            "code": "SYSTEM",
                            "tenantId": "pb"
                        }
                    ],
                    "tenantId": "pb.amritsar",
                    "uuid": "cdbba3bc-5d4f-4742-bbb7-418d8dfce7fd"
                }
            },
            "Payment": {
                "paymentDetails": [payment],
                "tenantId": tenant,
                "totalDue": self.totalamount,
                "paymentMode": paymentmode,
                "paidBy": ownerdata,
                "mobileNumber": mobile,
                "payerName": ownerdata,
                "totalAmountPaid": total_amount,
                "transactionNumber": transactionNumber,
                "instrumentDate":epoch_timestamp,
                "instrumentNumber": transactionNumber,
                "instrumentstatus": "APPROVED",
                "transactionDate": epoch_timestamp

            }
        }
            request_body_string = json.dumps(request_body)

            if iswaterrecepituploaded!='COMPLETED':
                receipt_response = requests.post(url, headers=headers, data=json.dumps(request_body))
                response_decoded = receipt_response.content.decode('utf-8')
                response_decoded = json.dumps(response_decoded, indent=2)
                print(receipt_response)
                if receipt_response.status_code==200:
                    update_query = """UPDATE ludhiana_split_receipt SET water_upload_status='COMPLETED', upload_water_req=%s,upload_water_res=%s,isreceiptwatermigrated='True' WHERE id_no=%s"""
                    params = (request_body_string, response_decoded, str(self.connno))
                    cursor_ws.execute(update_query, params)
                    update_query_watertable ="UPDATE ludhiana_ws_legacy_data SET iswaterdemandmigrated='True' WHERE pkwsid='"+str(self.connno)+"'"
                    cursor_ws.execute(update_query_watertable)
                    print(receipt_response)
                    data = receipt_response.json()
                    receipt_number = data["Payments"][0]["paymentDetails"][0]["receiptNumber"]

                    reciptupdatequery="update egcl_paymentdetail set receiptdate='"+str(epoch_timestamp)+"'  where receiptnumber='"+str(receipt_number)+"'; update egcl_payment set transactiondate='"+str(epoch_timestamp)+"'  where instrumentnumber='"+str(transactionNumber)+"';  "
                    reciptupdate_query = """UPDATE ludhiana_split_receipt SET water_receipt_datechange_query=%s WHERE id_no=%s"""
                    params = (reciptupdatequery, str(self.connno))
                    cursor_ws.execute(reciptupdate_query, params)
                    connection_db_ws.commit()
                    print("Water Receipt has been generated with amount " + str(total_amount))
                    print("Generated The receipt Of the Particular  Water connection No: " + self.connno)
                else:
                    update_query = "UPDATE ludhiana_split_receipt  SET water_upload_status='ERROR', upload_water_req='"+request_body_string+"', isreceiptwatermigrated='False' WHERE id_no='"+str(self.connno)+"'"
                    cursor_ws.execute(update_query)
                    connection_db_ws.commit()
                    print("Error While Generating The receipt of connection number: " + self.connno)
            else:
                print("Receipt has been already Migrated For this connection number")
        else:
            update_query_watertable = "UPDATE ludhiana_demand SET iswaterdemanduploaded='True' WHERE id_no='"+str(self.connno)+"'"
            cursor_ws.execute(update_query_watertable)
            update_query_watertable = "UPDATE ludhiana_ws_legacy_data SET iswaterdemandmigrated='True' WHERE pkwsid='"+str(self.connno)+"'"
            cursor_ws.execute(update_query_watertable)
            print("No Receipt present for this connection: " + self.connno)
# class updatereceipt:
#     def __init__(self,transactionNumber,connno,access_token):
#         self.connno = connno
#         self.access_token = access_token
#         self.transactionNumber = transactionNumber
#         self.receiptgenerator(self)
#
#     def updatereceipt(self, responses):
#         url=implementation_url+"collection-services/payments/WS/_search?tenantId="+tenant+"&consumerCodes=&businessService=WS&consumerCode="+self.connno
#         request_body = {
#                 'RequestInfo': {
#                     'apiId': 'Mihy',
#                     'ver': '.01',
#                     'action': '',
#                     'did': '1',
#                     'key': '',
#                     'msgId': '20170310130900|en_IN',
#                     'requesterId': '',
#                     "authToken": self.access_token
#                     }
#                 }
#         receiptr = requests.post(url, json=request_body)
connection_db_ws.commit()











