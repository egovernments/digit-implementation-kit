from common import *
import requests
from config.dbfile import *
import math
from datetime import datetime
class seweragedemand:
    def __init__(self, response,sewerageData):
        self.response = response
        self.sewerageData = sewerageData
        self.demandforsewerage(self,sewerageData)

    def demandforsewerage(self,responses,sewerageData):
        print ("Creating Demand For Sewerage")
        consumercode =self.sewerageData['id_no']
        taxperiodfrom= str('1680307200000')
        taxperiodto=str('1711909799000')
        old_taxperiodfrom = str('1648771200000')
        old_taxperiodto = str('1680287399000')
        payer =self.response['SewerageConnections'][0]['connectionHolders'][0]['uuid']
        selectquery="Select row_to_json(cd) from ludhiana_demand as cd where cd.id_no='"+consumercode+"'"
        cursor_ws.execute(selectquery)
        data = cursor_ws.fetchmany()
        if data:
            for row in data:
                json_data = row[0]
                sewerage_current = json_data["sewer_current"]
                connno=json_data["id_no"]
                sewerage_arrear_old=float(json_data["sewer_arrear"])
                sewerage_interest_old = float(json_data["sewer_interest_arrear"])

                sewerage_arrear = math.floor(sewerage_arrear_old)
                sewerage_arrear_decimal =sewerage_arrear_old - sewerage_arrear

                sewerage_interest = math.floor(sewerage_interest_old)
                sewerage_interest_decimal = sewerage_interest_old - sewerage_interest

                total_round=sewerage_arrear_decimal+sewerage_interest_decimal

                total_round_add = math.floor(total_round)
                total_addition = total_round - total_round_add
                if total_round_add>0:
                    sewerage_arrear=sewerage_arrear+total_round_add
                else:
                    sewerage_arrear = sewerage_arrear
                if total_addition>=0.5:
                    round_off="+"+str(round(total_addition, 2))
                else:
                    round_off = "-" + str(round(total_addition, 2))
                isdemanduploaded= json_data["isseweragedemanduploaded"]
                old_demand_query="Select  row_to_json(cd) from ludhiana_split_receipt as cd where cd.id_no='"+connno+"'"
                cursor_ws.execute(old_demand_query)
                old_data = cursor_ws.fetchmany()

                total_amount_data=0
                if data:
                    if old_data:
                        for rows in old_data:
                            json_data = rows[0]
                            amountpaid=int(json_data["current_sewerage_paid"])
                            sewerage_arrears = int(sewerage_arrear)
                            total_amount_data = sewerage_arrears + amountpaid
                    else:
                        total_amount_data = sewerage_arrear
                print("arrear sewerage amount " + str(total_amount_data))
                print("Current sewerage amount " + sewerage_current)
                old_due=total_amount_data+float(round_off)+sewerage_interest
                SW_CHARGE_NEW = {
                    "isPaymentCompleted": False,
                    "id": None,
                    "tenantId": self.response['SewerageConnections'][0]['tenantId'],
                    "consumerCode": self.response['SewerageConnections'][0]['connectionNo'],
                    "consumerType": "sewerageConnection",
                    "businessService": "SW",
                    "payer": {
                        "id": None,
                        "userName": self.response['SewerageConnections'][0]['connectionHolders'][0]['userName'],
                        "name": self.response['SewerageConnections'][0]['connectionHolders'][0]['name'],
                        "type": "CITIZEN",
                        "mobileNumber": self.response['SewerageConnections'][0]['connectionHolders'][0]['mobileNumber'],
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
                            "taxHeadMasterCode": "SW_CHARGE",
                            "taxAmount": sewerage_current,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['SewerageConnections'][0]['tenantId']
                        }

                    ],
                    "auditDetails": None,
                    "billExpiryTime": 2592000000,
                    "additionalDetails": None,
                    "minimumAmountPayable": sewerage_current,
                    "status": "ACTIVE"
                }
                old_demand={
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "SW_CHARGE",
                            "taxAmount": total_amount_data,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['SewerageConnections'][0]['tenantId']
                        }
                old_interest={
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "SW_TIME_INTEREST",
                            "taxAmount": sewerage_interest,
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['SewerageConnections'][0]['tenantId']
                        }
                old_roundoff= {
                            "id": None,
                            "demandId": None,
                            "taxHeadMasterCode": "SW_Round_Off",
                            "taxAmount": float(round_off),
                            "collectionAmount": 0,
                            "auditDetails": None,
                            "tenantId": self.response['SewerageConnections'][0]['tenantId']
                        }


                SW_CHARGE_old = {
                    "isPaymentCompleted": False,
                    "id": None,
                    "tenantId": self.response['SewerageConnections'][0]['tenantId'],
                    "consumerCode": self.response['SewerageConnections'][0]['connectionNo'],
                    "consumerType": "sewerageConnection",
                    "businessService": "SW",
                    "payer": {
                        "id": None,
                        "userName": self.response['SewerageConnections'][0]['connectionHolders'][0]['userName'],
                        "name": self.response['SewerageConnections'][0]['connectionHolders'][0]['name'],
                        "type": "CITIZEN",
                        "mobileNumber": self.response['SewerageConnections'][0]['connectionHolders'][0]['mobileNumber'],
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
                    "Demands": [SW_CHARGE_NEW,SW_CHARGE_old]
                }
                request_body_string = json.dumps(request_body)

            if isdemanduploaded=='False':
                demand_response = requests.post(url, headers=headers, data=json.dumps(request_body))
                response_decoded = demand_response.content.decode('utf-8')
                response_decoded = json.dumps(response_decoded, indent=2)
                if demand_response.status_code==201:
                    print("Sewerage Demand Has Been Created Successfully")
                    print("Response Code is 200(New Deamand Created) of connection No "+connno)
                    update_query = "UPDATE ludhiana_demand SET  sewerage_upload_status='COMPLETED',upload_sewerage_req = '"+request_body_string+"',upload_sewerage_response = '"+response_decoded+"',isseweragedemanduploaded='True' WHERE id_no = '"+str(connno)+"';"
                    cursor_ws.execute(update_query)
                    fetchbill(connno)
                elif demand_response.status_code == 400:
                    print("Response Code is 400( Deamand already present ) of connection No "+connno)
                    update_query = "UPDATE ludhiana_demand SET  sewerage_upload_status='COMPLETED',upload_sewerage_req = '" + request_body_string + "',upload_sewerage_response = '" + response_decoded + "',isseweragedemanduploaded='True' WHERE id_no = '" + str(
                        connno) + "';"
                    cursor_ws.execute(update_query)
                    print("Sewerage Demand is already present for given connection")
                    fetchbill(connno)
                else:
                    update_query = "UPDATE ludhiana_demand SET sewerage_upload_status='ERROR', upload_sewerage_req=%s, isdemanduploaded='False' WHERE id_no=%s"
                    params = (request_body_string, str(connno))

                    # Execute the query with parameters
                    cursor_ws.execute(update_query, params)

                    print("Sewerage Demand is not present for this connection")
        else:

            print("DEMAND IS ALREADY PRESENT FOR GIVEN CONNECTION NUMBER")



class fetchbill:
    def __init__(self,response):
        self.response = response
        self.fetchbill(self)

    def fetchbill(self, response):
        print("Going To fetch the bill for the particular Sewearge Connection : "+self.response)
        url = implementation_url+"billing-service/bill/v2/_fetchbill?tenantId="+tenant+"&consumerCode="+self.response+"&businessService=SW"
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

        bill_response = requests.post(url, headers=headers, data=json.dumps(request_body))
        json_data = bill_response.json()

        # Check if "Bill" array has data
        if json_data["Bill"]:
            bill_id = json_data["Bill"][0]["id"]
            amount = json_data["Bill"][0]["totalAmount"]
            print("Bill Id for this Particular Sewerage Demand Is: "+bill_id)
            print("Total Sewerage Demand Amount: "+str(amount))
            print("Going To Generate The receipt Of the Particular Sewerage connection No: "+ self.response)
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
        url = implementation_url+"collection-services/payments/_create?"
        headers = {
            "Content-Type": "application/json",
        }
        access_token = superuser_login()["access_token"]
        receipt_query = "Select  row_to_json(cd) from ludhiana_split_receipt as cd where cd.id_no='" + self.connno + "'"
        cursor_ws.execute(receipt_query)
        data = cursor_ws.fetchmany()
        if data:
            for row in data:
                json_data = row[0]
                current_arrear_sewerage_paid = int(json_data["current_arrear_sewerage_paid"])
                current_arrear_sewerage_interest_paid =int(json_data["current_arrear_sewerage_int_paid"])
                current_sewerage_paid = int(json_data["current_sewerage_paid"])
                total_amount = current_arrear_sewerage_paid + current_arrear_sewerage_interest_paid + current_sewerage_paid
                reciept_book_no =  json_data["g8_book_no"]
                transactionNumber = json_data["transaction_id"]
                reciept_date = json_data["payment_date"]
                date_format = '%d-%m-%Y'
                date_object = datetime.strptime(reciept_date, date_format)
                epoch_timestamp = int(date_object.timestamp())
                receipt_no = json_data["g8_receipt_no"]
                paymentmode = json_data["payment_mode"]
                isseweragerecepituploaded = json_data["isreceiptwatermigrated"]
                if receipt_no != None and reciept_book_no != None:
                    reciept_book_no = reciept_book_no + "/" + receipt_no
                    payment = {
                        "manualReceiptDate": epoch_timestamp,
                        "manualReceiptNumber": reciept_book_no,
                        "businessService": "SW",
                        "billId": self.billid,
                        "totalDue": self.totalamount,
                        "totalAmountPaid": total_amount
                    }

                else:
                    payment = {
                        "businessService": "SW",
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
            mobile = json_data["mobile"]
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
                    "instrumentDate": epoch_timestamp,
                    "instrumentNumber": transactionNumber,
                    "instrumentstatus": "APPROVED",
                    "transactionDate": epoch_timestamp
                }
            }
            request_body_string = json.dumps(request_body)
            if isseweragerecepituploaded!= 'COMPLETED':
                receipt_response = requests.post(url, headers=headers, data=json.dumps(request_body))
                if receipt_response.status_code==200:
                    
                    response_decoded = receipt_response.content.decode('utf-8')
                    response_decoded = json.dumps(response_decoded, indent=2)
                    update_query = "UPDATE ludhiana_split_receipt SET sewerage_upload_status='COMPLETED', upload_sewerage_req='"+request_body_string+"', upload_sewerage_res='"+response_decoded+"', isreceiptseweragemigrated='True' WHERE id_no='"+str(self.connno)+"';"
                    update_query_seweragetable = "UPDATE ludhiana_ws_legacy_data SET isseweragedemandmigrated='True' WHERE pkwsid='"+str(self.connno)+"';"
                    cursor_ws.execute(update_query)
                    cursor_ws.execute(update_query_seweragetable)

                    data = receipt_response.json()
                    receipt_number = data["Payments"][0]["paymentDetails"][0]["receiptNumber"]
                    print("Receipt Number:", receipt_number)
                    reciptupdatequery = "update egcl_paymentdetail set receiptdate='" + str(epoch_timestamp) + "'  where receiptnumber='" + str(receipt_number) + "'; update egcl_payment set transactiondate='" + str(epoch_timestamp) + "'  where instrumentnumber='" + str(transactionNumber) + "';  "
                    reciptupdate_query = """UPDATE ludhiana_split_receipt SET sewerage_receipt_datechange_query=%s WHERE id_no=%s"""
                    params = (reciptupdatequery, str(self.connno))
                    cursor_ws.execute(reciptupdate_query, params)

                    print("Generated The receipt Of the Particular sewerage connection No: " + self.connno)
                else:
                    update_query ="UPDATE ludhiana_split_receipt SET sewerage_upload_status='ERROR', upload_sewerage_req='"+request_body_string+"', isreceiptseweragemigrated='False' WHERE id_no='"+ str(self.connno)+"';"
                    cursor_ws.execute(update_query)
                    connection_db_ws.commit()
                    print("Error While Generating The receipt of connection number: " + self.connno)
                    print(request_body)
                    print(receipt_response.json())
            else:
                update_query_seweragetable = "UPDATE ludhiana_demand SET isseweragedemanduploaded='True' WHERE id_no='"+str(self.connno)+"';"
                cursor_ws.execute(update_query_seweragetable)
                update_query_seweragetable = "UPDATE ludhiana_ws_legacy_data SET isseweragedemandmigrated='True' WHERE pkwsid='"+str(self.connno)+"';"
                cursor_ws.execute(update_query_seweragetable)
                print("Receipt has been already Migrated For this connection number")
        else:
            update_query_seweragetable ="UPDATE ludhiana_demand SET isseweragedemanduploaded='True' WHERE id_no='"+str(self.connno)+"';"
            cursor_ws.execute(update_query_seweragetable)
            update_query_seweragetable = "UPDATE ludhiana_ws_legacy_data SET isseweragedemandmigrated='True' WHERE pkwsid='"+str(self.connno)+"';"
            cursor_ws.execute(update_query_seweragetable)
            print("No Receipt present for this connection: " + self.connno)


connection_db_ws.commit()











