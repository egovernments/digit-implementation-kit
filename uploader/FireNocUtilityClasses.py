import json
from typing import Optional, List
from urllib.parse import urljoin
from uuid import UUID

class FireNocDetails:
    def __init__(self,context, district:Optional[str]=None, subdistrict:Optional[str]=None,
                 firestation_id:Optional[str]=None) -> None:

        self.no_of_buildings=context["no_of_buildings"]
        self.fireNOC_type=context["noc_type"].upper()
        self.firestation_id=firestation_id
        self.action="INITIATE"
        self.channel="COUNTER"
        self.financial_year="2019-20"
        self.tenant_id=subdistrict
        self.process_additional_details(context)  # will be member of firenocdetails.applicantdetails
        self.process_propertydetails(context, district, subdistrict)  # will be member of firenocdetails
        self.process_applicantdetails(context)
        self.process_buildings(context)
        #self.buildings: Optional[List[Building]] = None
        #self.buildings=[]
        #self.buildings.append(Building(context))
        # self.property_details = property_details
        #self.process_additional_details(context)
        #self.process_propertydetails(context,district,subdistrict)

    def process_additional_details(self, context):
        self.additional_detail = {
            "lagacyInfo": {
                "applicationid": context["application_id"],
                "no_of_buildings": context["no_of_buildings"],
                "noc_type": context["noc_type"],
                "building_address": context["building_address"],
                "areatype":context["areatype"],
                "city":context["city"],
                "subdistrict":context["subdistrict"],
                "localitycode":context["localitycode"],
                "firestationid":context["firestationid"],
                "name_of_building":context["name_of_building"],
                "usagetype":context["usagetype"],
                "usagesubtype":context["usagesubtype"],
                "height_of_building":context["height_of_building"],
                "number_of_actual_floors":context["number_of_actual_floors"],
                "number_of_basement":context["number_of_basements"],
                "builtup_area":context["builtup_area"],
                "land_area":context["land_area"],
                "covered_area_total":context["covered_area_total"],
                "parking_area":context["parking_area"],
                "left_surrounding":context["left_surrounding"],
                "right_surrounding": context["right_surrounding"],
                "front_surrounding": context["front_surrounding"],
                "back_surrounding": context["back_surrounding"],
                "date_of_approval":context["date_of_approval"],
                "date_of_submission":context["date_of_submission"],
                "old_noc_no":context["old_noc_no"],
                "new_noc_no": context["new_noc_no"],
                "unique_application_id":context["unique_application_id"],
                "owner_name":context["owner_name"],
                "owner_address":context["owner_address"],
                "applicant_contact_no":context["applicant_contact_no"]
            },
            "documents":[]
        }
    def process_propertydetails(self, context, district,subdistrict):
        locality = Locality(code=context["localitycode"])
        #self.address = Address(city=city, door_no=context["houseno"], locality=locality)
        #street allowed upto 254 charcaters only in api
        address = Address(district=district, sub_district=subdistrict, street=context["building_address"][:254], locality=locality,area_type=context["areatype"])
        self.property_details=PropertyDetails( address)
    def process_applicantdetails(self,context):
        self.applicant_details=ApplicantDetails(context)
    def process_buildings(self,context):
        self.buildings = [
            {
            "name": context["name_of_building"],
            "usageType": context["usagetype"],
            "usageSubType": context["usagesubtype"],
            "uomsMap": {
                "NO_OF_FLOORS": int(context["number_of_actual_floors"]),
                "BUILTUP_AREA": float(context["builtup_area"]),
                "NO_OF_BASEMENTS": int(context["number_of_basements"]),
                "HEIGHT_OF_BUILDING": int(float(context["height_of_building"]))

            },
            "landArea": float(context["land_area"]),
            "totalCoveredArea": float(context["covered_area_total"]),
            "leftSurrounding": context["left_surrounding"],
            "rightSurrounding": context["right_surrounding"],
            "frontSurrounding": context["front_surrounding"],
            "backSurrounding": context["back_surrounding"],
            "parkingArea": float(context["parking_area"]),
            "uoms": [
                {
                    "code": "HEIGHT_OF_BUILDING",
                    "value": int(float(context["height_of_building"])),
                    "isActiveUom": True,
                    "active": True
                },
                {
                    "code": "NO_OF_FLOORS",
                    "value": int(context["number_of_actual_floors"]),
                    "isActiveUom": False,
                    "active": True
                },
                {
                    "code": "NO_OF_BASEMENTS",
                    "value": int(context["number_of_basements"]),
                    "isActiveUom": False,
                    "active": True
                },
                {
                    "code": "BUILTUP_AREA",
                    "value": int(float(context["covered_area_total"])),
                    "isActiveUom": False,
                    "active": True
                }
            ],
            "applicationDocuments": []
        }
        ]




class Locality:
    code: Optional[str]

    def __init__(self, code: Optional[str] = None) -> None:
        self.code = code



class Address:
    area_type: Optional[str]
    city: Optional[str]
    sub_district: Optional[str]
    street: Optional[str]
    locality: Optional[Locality]


    def __init__(self,  district: Optional[str] = None, sub_district: Optional[str] = None,
                 street: Optional[str] = None, locality: Optional[Locality] = None,
                 area_type: Optional[int] = None) -> None:
        self.city = district
        self.sub_district=sub_district
        self.area_type = area_type
        self.street = street
        self.locality = locality

class PropertyDetails:
    address: Optional[str]

    def __init__(self,adr:Optional[str] =None):
        self.address=adr


class ApplicantDetails:
    def __init__(self,context):
        self.owner_ship_major_type ="INDIVIDUAL"
        self.owner_ship_type = "INDIVIDUAL.SINGLEOWNER"
        self.owners: Optional[List[Owner]] #owners is array of Owner objects
        self.owners=[]

        self.processOwners(context)
        self.process_additional_details()
    def processOwners(self,context):
        owner=Owner(context["owner_name"],mobile_number=context["applicant_contact_no"],father_or_husband_name="NA",relationship="FATHER",owner_type="NONE",gender="MALE",correspondence_address=context["owner_address"])
        self.owners.append(owner)
    def process_additional_details(self):
        owner_auditional_detail=OwnerAuditionalDetail()
        self.additional_detail=OwnerAdditionalDetail(owner_auditional_detail)


class OwnerAdditionalDetail:
    def __init__(self,OwnerAuditionalDetail):
        self.owner_auditional_detail=OwnerAuditionalDetail

class OwnerAuditionalDetail:
    def __init__(self):
        self.documents=[]







class Owner:
    mobile_number: Optional[str]
    name: Optional[str]
    corresondence_address: Optional[str]
    gender: Optional[str]
    dob: Optional[str]
    relationship: Optional[str]
    father_or_husband_name: Optional[str]
    owner_type: Optional[str]

    def __init__(self, name: Optional[str] = None,
                 mobile_number: Optional[str] = None,  father_or_husband_name: Optional[str] = None,
                 relationship: Optional[str] = None, owner_type: Optional[str] = None,
                 gender: Optional[str] = None, correspondence_address: Optional[str] = None
                 ) -> None:
        self.dob=946665000000  # 01-01-2000
        self.name = name
        self.mobile_number = mobile_number
        self.father_or_husband_name = father_or_husband_name
        self.relationship = relationship
        self.owner_type = owner_type
        self.gender = gender
        self.correspondence_address = correspondence_address

