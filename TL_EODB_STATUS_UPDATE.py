import requests
import json
from datetime import date
from datetime import datetime
import pytz

token = None
access_token = None
response1 = None
mSevaURL = 'http://mseva.lgpunjab.gov.in'
mSevaEmpid = 'EMP9'
mSevaPassword = 'eGov@123'
mSevaEmpTenant = 'pb.testing'

# ---------------------------- for current Date----------------------------
today = date.today()
s = json.dumps(today, default=str)
s1 = s.replace('"', "")
print("Push TL EODB Records Started At   " + str(datetime.now(pytz.timezone('Asia/Kolkata'))))
print(
    "----------------------------------------------------------------------------------------------------------------")
# print (s)


# def loginUserMseva(empid,pwd,tenant):
STATUS_DESC_MAP = {
    "APPLIED": "Form Submitted(Created)",
    "PENDINGPAYMENT": "Payment Raised(Estimation Notice Generated)",
    "INITIATED": "Payment Raised(Estimation Notice Generated)",
    "CANCEL": "Rejected",
    "CANCELLED": "Rejected",
    "REJECTED": "Rejected",
    "APPROVED": "Clearance Issued",
    "PAID": "Fees Paid(Estimation amount paid)",
    "CITIZENACTIONREQUIRED": "Objection Raised",
    "FIELDINSPECTION": "Form Submitted(Created)"
}

STATUS_CODE_MAP = {
    "Form Submitted(Created)": "1",
    "Payment Raised(Estimation Notice Generated)": "2",
    "Rejected": "3",
    "Clearance Issued": "4",
    "Fees Paid(Estimation amount paid)": "5",
    "Objection Raised": "6",

}


# ------ function to fetch auth token from mSeva-----------------------------
def msevatoken(un, pwd, tenant):
    url = mSevaURL + "/user/oauth/token"
    payload = 'username=' + un + '&password=' + pwd + '&grant_type=password&scope=read&tenantId=' + tenant + '&userType=EMPLOYEE'

    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": "Basic ZWdvdi11c2VyLWNsaWVudDplZ292LXVzZXItc2VjcmV0"}

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()
    # print(json_response)
    # print(response.text)
    # global access_token  # telling that token is not creatd to be local but to be used global in this function
    if "access_token" in json_response:
        access_token = json_response["access_token"]
        # print (access_token,"token granted")
    else:
        print("unable to login to mseva: ", json_response)
        access_token = None
    return access_token


# msevatoken(access_token)


# ----------------------- to fetch data from EODB -----------------------

def fetchEODBRecordsFromMseva():
    mseva_token = msevatoken(mSevaEmpid, mSevaPassword, mSevaEmpTenant)
    if mseva_token is None:
        exit(0)
    # print(a,"new")
    # print(a)
    url = mSevaURL + "/egov-searcher/rainmaker-pt-gissearch/searchTLApplicationsEODB/_get"
    payload = json.dumps({
        "RequestInfo": {
            "apiId": "Rainmaker",
            "ver": ".01",
            "action": "",
            "did": "1",
            "key": "",
            "msgId": "20170310130900|en_IN",
            "requesterId": "",
            "authToken": mseva_token
        },
        "searchCriteria": {}
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ZWdvdi11c2VyLWNsaWVudDplZ292LXVzZXItc2VjcmV0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()

    response = requests.request("POST", url, headers=headers, data=payload)
    response1 = response
    # print(a,"token is here")
    # print(response1.text)
    print()
    print()
    for application in response.json()["data"]:
        print("TL Application:", application["applicationnumber"], "                EODB App Id:", application["ipin"],
              "                  EODB IPin :", application["ipin"])

    return response1


# fetchEODBRecordsFromMseva()


# ---------------------- TO access Token from EODB-------------------------
def getToken():
    url = "https://pbindustries.gov.in/testportalnode/api/iptoken/gettoken"
    payload = json.dumps({
        "IntegrationKey": "UAT_LG"})
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()
    # print(response.text)
    global token  # telling that token is not creatd to be local but to be used global in this function
    if "token" in json_response:
        token = json_response["token"]
        # print (token)
    else:
        print("unable to get login token, error is: " + json_response["msg"])
        token = None


# -----------------------updatation in EODB----------------------------------------


def updatePush():
    m1 = fetchEODBRecordsFromMseva()

    # data123 = json.loads(m1)

    # print(ipin)
    # print(appid)
    # print(status)

    # print(m1)
    global token  # telling that token is not local but to be used global in this function
    if token is None:  # try to get authorization token if token is None
        getToken()
    if token is None:  # if token in still None, i.e. unable to get token from EODB site then exit
        exit(0)

    for i in m1.json()["data"]:
        appid = i["appid"],
        s2 = appid[0].replace("'", "")
        print()
        print(s2)
        status = i["status"]
        print(status)
        ipin = i["ipin"]
        print(ipin)
        status_description = STATUS_DESC_MAP[status]
        status_code = STATUS_CODE_MAP[status_description]
        url = "https://pbindustries.gov.in/testportalnode/api/lgtrade/UpdateStatus"
        head = {"Content-Type": "application/json", "Authorization": token}
        data1 = {
            "iPin": ipin,
            "AppId": s2,
            "statusId": status_code,
            "statusDesc": status_description,
            "comments": "NA",
            "senderName": "PAWAN BANSAL",
            "senderDesignation": "NA",
            "receiverName": "NA",
            "receiverDesignation": "NA",
            "clearanceIssuedOn": "NA",
            "clearanceExpiredOn": "NA",
            "licenseNo": "NA",
            "clearanceFile": "NA",
            "statusDate": s1,
            "integrationSource": "LG",
            "deemedApproval": "false"
        }
        response = requests.post(url, data=json.dumps(data1), headers=head)
        response_dict = json.loads(response.text)
        print("REQUEST DATA= ", data1);
        print();
        print("RESPONSE=", response_dict);
        print();
        print();
        # print(s1)
        # for i in response_dict:
        #    print("key: ", i, "val: ", response_dict[i])


updatePush()