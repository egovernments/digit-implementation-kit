import json
from typing import Optional, List
from urllib.parse import urljoin
from uuid import UUID
import requests

from config import config
from uploader.parsers.utils import PropertyEncoder, convert_json, underscore_to_camel


from FireNocUtilityClasses import *


class FireNocRecord:

    def __init__(self, *args, **kwargs):
        print("creating Application Object ")

    def process_record(self,context,district,subdistrict,firestation_id):
        self.tenant_id=subdistrict
        self.is_legacy= True
        self.process_firenocdetails(context,district,subdistrict,firestation_id)
    def process_firenocdetails(self,context,district:Optional[str]=None, subdistrict:Optional[str]=None,firestation_id:Optional[str]=None):
        self.fireNOCDetails=FireNocDetails(context,district,subdistrict, firestation_id)
    def upload_Application(self,access_token:Optional[str]=None):
        request_data = {
            "RequestInfo": {
                "apiId": "Mihy",
                "ver": ".01",
                "action": "",
                "did": "1",
                "key": "",
                "msgId": "20170310130900|en_IN",
                "requesterId": "",
                "authToken": access_token
            },
            "FireNOCs": [ self.get_application_json() ]
        }
        # print(json.dumps(request_data, indent=2))
        response = requests.post(
            urljoin(config.HOST, "/firenoc-services/v1/_create?"),
            json=request_data)
        print("request is ",request_data)

        res = response.json()

        return request_data, res

    def get_application_json(self):
        property_encoder = PropertyEncoder().encode(self)
        return convert_json(json.loads(property_encoder), underscore_to_camel)


