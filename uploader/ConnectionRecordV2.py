import json
from typing import Optional, List
from urllib.parse import urljoin
from uuid import UUID
from uploader.PropertyTaxV2 import Property

import requests

from config import config
from uploader.parsers.utils import PropertyEncoder, convert_json, underscore_to_camel

class ConnectionRecord:
    tenant_id: Optional[str]