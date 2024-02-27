our first try will be to migrate the ludhiana connections which are mapped with unique property id by ludhiana MC, and as property search API is not equiped with search by surveyid (migrated unique propertyid by ludhiana) we will fetch the propery with old property id and will fit the Property response to WS create request payload
property search end point to search through old propertyid: 
{{url}}/property-services/property/_search?oldpropertyids=RID306389&tenantId=pb.ludhiana
username = "atul23"
password = "eGov@123"
tenant_id = "pb.ludhiana"

{{url}}/ws-services/wc/_create  creates water connection
{
  "RequestInfo": {
    "apiId": "Rainmaker",
    "ver": ".01",
    "action": "_create",
    "did": "1",
    "key": "",
    "msgId": "20170310130900|en_IN",
    "requesterId": "",
    "authToken": "1937da2a-19c5-45f0-ba0e-5e329004c67e"
  },
  "WaterConnection": {
    "water": true,
    "sewerage": false,
    "connectionHolders": null,
    "property": {
            "id": "cff0efd0-8fe3-4d84-821c-26d682834cb7",
            "propertyId": "PT-1211-1629357",
            "surveyId": "B027-00394",
            "linkedProperties": null,
            "tenantId": "pb.ludhiana",
            "accountId": "356502f0-f499-43a2-ae09-b95c97d7177d",
            "oldPropertyId": "RID306389",
            "status": "ACTIVE",
            "address": {
                "tenantId": "pb.ludhiana",
                "doorNo": "208/1452-D",
                "plotNo": null,
                "id": "04bd5146-3828-468c-8d3a-1161ae1fb9c0",
                "landmark": null,
                "city": "LUDHIANA",
                "district": null,
                "region": null,
                "state": null,
                "country": null,
                "pincode": null,
                "buildingName": null,
                "street": null,
                "locality": {
                    "code": "Ldh_837",
                    "name": "MODEL TOWN EXTN PART-2 (TP SCHEME) (MODEL TOWN LIT PART-II) - D27 - A3",
                    "label": "Locality",
                    "latitude": null,
                    "longitude": null,
                    "area": "AREA3",
                    "children": [],
                    "materializedPath": null
                },
                "geoLocation": {
                    "latitude": 0.0,
                    "longitude": 0.0
                },
                "additionalDetails": null
            },
            "acknowldgementNumber": "AC-2023-12-21-1630072",
            "propertyType": "BUILTUP.INDEPENDENTPROPERTY",
            "ownershipCategory": "INDIVIDUAL.SINGLEOWNER",
            "owners": [
                {
                    "id": null,
                    "uuid": "0085957b-104d-4fed-a6d4-10f06ee4a8dd",
                    "userName": "95c107b3-afef-4b3b-8edb-789be56aff90",
                    "password": null,
                    "salutation": null,
                    "name": "SURINDER SINGH",
                    "gender": "MALE",
                    "mobileNumber": "9814476879",
                    "emailId": null,
                    "altContactNumber": null,
                    "pan": null,
                    "aadhaarNumber": null,
                    "permanentAddress": null,
                    "permanentCity": null,
                    "permanentPinCode": null,
                    "correspondenceCity": null,
                    "correspondencePinCode": null,
                    "correspondenceAddress": null,
                    "active": true,
                    "dob": null,
                    "pwdExpiryDate": 1710953664000,
                    "locale": null,
                    "type": "CITIZEN",
                    "signature": null,
                    "accountLocked": false,
                    "roles": [
                        {
                            "id": null,
                            "name": "Citizen",
                            "code": "CITIZEN",
                            "tenantId": "pb"
                        }
                    ],
                    "fatherOrHusbandName": "SHER SINGH",
                    "bloodGroup": null,
                    "identificationMark": null,
                    "photo": null,
                    "createdBy": "1243690",
                    "createdDate": 1703177664000,
                    "lastModifiedBy": "1",
                    "lastModifiedDate": 1703177666000,
                    "tenantId": "pb",
                    "ownerInfoUuid": "95141a4d-aa39-4bd4-9228-dfcd28fc6013",
                    "isPrimaryOwner": null,
                    "ownerShipPercentage": null,
                    "ownerType": "NONE",
                    "institutionId": null,
                    "status": "ACTIVE",
                    "documents": null,
                    "relationship": "FATHER"
                }
            ],
            "institution": null,
            "creationReason": "CREATE",
            "usageCategory": "RESIDENTIAL",
            "noOfFloors": 1,
            "landArea": 125.0,
            "superBuiltUpArea": null,
            "source": "LEGACY_RECORD",
            "channel": "LEGACY_MIGRATION",
            "documents": null,
            "units": [
                {
                    "id": "42448028-341f-464e-8827-0e25c271f0d2",
                    "tenantId": null,
                    "floorNo": 0,
                    "unitType": null,
                    "usageCategory": "RESIDENTIAL",
                    "occupancyType": "SELFOCCUPIED",
                    "active": true,
                    "occupancyDate": 0,
                    "constructionDetail": {
                        "carpetArea": null,
                        "builtUpArea": 125,
                        "plinthArea": null,
                        "superBuiltUpArea": null,
                        "constructionType": null,
                        "constructionDate": null,
                        "dimensions": null
                    },
                    "additionalDetails": null,
                    "auditDetails": null,
                    "arv": null
                }
            ],
            "additionalDetails": {
                "legacyInfo": {
                    "colony": "MODEL TOWN EXTN PART-2 (TP SCHEME) (MODEL TOWN LIT PART-II)",
                    "sector": "27",
                    "taxamt": "812.00",
                    "session": "2013-2014",
                    "grosstax": "604.68",
                    "returnid": "306389",
                    "propertyuid": "B027-00394",
                    "totalcoveredarea": "1125.00",
                    "acknowledgementno": "130627682853523000",
                    "exemptioncategory": "Non-Exempted"
                }
            },
            "auditDetails": {
                "createdBy": "356502f0-f499-43a2-ae09-b95c97d7177d",
                "lastModifiedBy": "356502f0-f499-43a2-ae09-b95c97d7177d",
                "createdTime": 1703177664588,
                "lastModifiedTime": 1703177666137
            },
            "workflow": null
        },
    "service": "Water And Sewerage",
    "roadCuttingArea": null,
    "proposedWaterClosets": null,
    "proposedToilets": null,
    "noOfTaps": null,
    "noOfWaterClosets": null,
    "noOfToilets": null,
    "proposedTaps": null,
    "propertyId": "PT-1211-1629357",
    "additionalDetails": {
      "initialMeterReading": null,
      "detailsProvidedBy": "",
      "isexempted": false,
      "billingType": null,
      "billingAmount": null,
      "connectionCategory": null,
      "ledgerId": null,
      "avarageMeterReading": null,
      "meterMake": null,
      "compositionFee": null,
      "userCharges": null,
      "othersFee": null,
      "unitUsageType": null,
      "adhocPenalty": null,
      "adhocPenaltyComment": null,
      "adhocPenaltyReason": null,
      "adhocRebate": null,
      "adhocRebateComment": null,
      "adhocRebateReason": null,
      "estimationFileStoreId": null,
      "sanctionFileStoreId": null,
      "estimationLetterDate": null,
      "locality": "Ldh_837"
    },
    "tenantId": "pb.ludhiana",
    "processInstance": {
      "action": "INITIATE"
}
}
}

copy new assigned property ids from pt_legacy table to ws_legacy table
UPDATE ludhiana_ws_legacy_data as ws
SET new_propertyid = p.new_propertyid
FROM ludhiana_pt_legacy_data p
WHERE ws.uidno = p.propertyuid
  AND p.upload_status='COMPLETED'

to migrate water/sewerage records for records having mapped propertyuid by ludhiana for water and sewerage

create local database table for ws records
CREATE TABLE ludhiana_ws_legacy_data
(
  pkwsid text,
  block text,
  propertyno text,
  ownername text,
  mobile text,
  uidno text,
  email text,
  remarks text,
  tariff_type text,
  conn_type text,
  disconn_status text,
  exempted text,
  area_in_sqy text,
  new_propertyid text,
  batchname text,
  upload_status text,
  upload_req text,
  upload_res text,
  query_activate text,
  uuid text default uuid_generate_v4()
)

import from excel upto field area_in_sqy in above table

copy new assigned property ids from pt_legacy table to ws_legacy table
UPDATE ludhiana_ws_legacy_data as ws
SET new_propertyid = p.new_propertyid
FROM ludhiana_pt_legacy_data p
WHERE ws.uidno = p.propertyuid
  AND p.upload_status='COMPLETED'

distribute batches in ws table
update ludhiana_ws_legacy_data ws set batchname =('{1,2,3,4,5,6,7,8,9,10}'::text[])[ceil(random()*10)] where upload_status is null and ws.new_propertyid is not null;

