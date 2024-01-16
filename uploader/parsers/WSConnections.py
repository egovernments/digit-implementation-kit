import re

from uploader.PropertyTaxV2 import *
from uploader.ConnectionRecordV2 import *

from uploader.parsers.utils import *

owner_pattern = re.compile("(?<![DSNMW])/(?![OSA])", re.I)

class WSConnection(ConnectionRecord):
    def __init__(self, *args, **kwargs):
        super(WSConnection, self).__init__()
        self.owners = []
        self.survey_id=None