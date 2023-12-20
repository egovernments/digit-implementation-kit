import requests
import json

mSevaURL = 'http://localhost:1234'

# ------ function to decrypt name, mobilenumber and guardian name from mseva encryption service-----------------------------

def mseva_decrypt(name,mobilenumber,guardian):
    url = mSevaURL + "/egov-enc-service/crypto/v1/_decrypt"
    #payload = 'username=' + un + '&password=' + pwd + '&grant_type=password&scope=read&tenantId=' + tenant + '&userType=EMPLOYEE'
    payload = '[ {"userObject": { "mobileNumber": "'+mobilenumber+'", "name": "'+name+'", "guardian":"'+guardian+'"   }  }]'

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic ZWdvdi11c2VyLWNsaWVudDplZ292LXVzZXItc2VjcmV0"}

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()
    # print(json_response)
    # print(response.text)
    # global access_token  # telling that token is not creatd to be local but to be used global in this function
    if "userObject" in json_response[0]:
        name_dec = json_response[0]["userObject"]["name"]
        mobilenumber_dec = json_response[0]["userObject"]["mobileNumber"]
        guardian_dec = json_response[0]["userObject"]["guardian"]
        # print (access_token,"token granted")
    else:
        name_dec="fail"
        mobilenumber_dec="fail"
        guardian_dec="fail"
    values_dec=[name_dec,mobilenumber_dec,guardian_dec]
    return values_dec


fs = open("f:/property_owners_encrypted_part_1.csv", "rt")
fd=open("f:/property_owners_decryted_part_1.csv","wt")
fs.readline() # Skip first line as header line
count=0
for line in fs:
    #line=fs.readline()
    print ("record : ",count)
    try:
        line=line.replace('"','')
        line=line.replace('\n','')
        values=line.split(",")
        if  values[5].upper()=='NULL':
            values[5]='30048|20XTtrm6DnGxKOzYxy7h6k++5HA=' #encrypted value for NULL in gyardiad
        decrypted_values=mseva_decrypt(values[3],values[4],values[5])
        fd.write("\n"+values[0]+","+values[1]+","+values[2]+","+decrypted_values[0]+","+decrypted_values[1]+","+decrypted_values[2])
    except:
        print("........................error for ",values[2])
    count=count+1
fs.close()
fd.close()