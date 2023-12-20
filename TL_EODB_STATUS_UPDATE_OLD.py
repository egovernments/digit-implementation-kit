import requests
import json

token = None

#def loginUserMseva(empid,pwd,tenant):


def fetchEODBRecordsFromMseva():
    url = "https://mseva-uat.lgpunjab.gov.in/egov-searcher/rainmaker-pt-gissearch/searchTLApplicationsEODB/_get"
    payload = json.dumps({
        "RequestInfo": {
            "apiId": "Rainmaker",
            "ver": ".01",
            "action": "",
            "did": "1",

            "key": "",
            "msgId": "20170310130900|en_IN",
            "requesterId": "",
            "authToken": "c3a83ae7-1ff5-4198-b2ba-3dfbf8d882b0"
        },
        "searchCriteria": {}
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ZWdvdi11c2VyLWNsaWVudDplZ292LXVzZXItc2VjcmV0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



def getToken():
    url = "https://pbindustries.gov.in/testportalnode/api/iptoken/gettoken"
    payload = json.dumps({
        "IntegrationKey": "UAT_LG"})
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response=response.json()
    #print(response.text)
    global token  # telling that token is not creatd to be local but to be used global in this function
    if "token" in json_response:
        token = json_response["token"]
        print (token)
    else:
        print("unable to get login token, error is: " + json_response["msg"])
        token = None


def updatePush():
    global token # telling that token is not local but to be used global in this function
    if token is None: # try to get authorization token if token is None
        getToken()
    if token is None:  # if token in still None, i.e. unable to get token from EODB site then exit
        exit(0)

    url = "https://pbindustries.gov.in/testportalnode/api/lgtrade/UpdateStatus"
    head =  {"Content-Type":"application/json","Authorization": token}
    data1 = {
            "iPin": "19061600",
               "AppId": "2210794997",
               "statusId": 45,
               "statusDesc": "Application Executed",
               "comments": "NA",
               "senderName": "PAWAN BANSAL",
               "senderDesignation": "NA",
               "receiverName": "NA",
               "receiverDesignation": "NA",
               "clearanceIssuedOn": "NA",
               "clearanceExpiredOn": "NA",
               "licenseNo": "NA",
               "clearanceFile": "NA",
               "statusDate": "2022-01-22",
               "integrationSource": "LG",
               "deemedApproval":"false"
       }
    response = requests.post(url, data=json.dumps(data1), headers=head)
    response_dict = json.loads(response.text)
    for i in response_dict:
        print("key: ", i, "val: ", response_dict[i])

updatePush()