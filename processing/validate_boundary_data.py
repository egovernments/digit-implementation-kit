import json
import os
from pathlib import Path

from common import superuser_login, validate_boundary_data
from config import config

boundary_path = config.MDMS_LOCATION / config.CITY_NAME.lower() / "egov-location" / "boundary-data.json"

auth_token = superuser_login()["access_token"]


def process_boundary(auth_token):
    print("MDMS LOCATION : {}".format(config.MDMS_LOCATION))
    print("ENV : {}\n".format(config.CONFIG_ENV))

    for folder in os.scandir(config.MDMS_LOCATION):
        boundary_path = Path(folder.path) / "egov-location" / "boundary-data.json"

        if os.path.isfile(boundary_path):

            with open(boundary_path) as f:
                boundary_data = json.load(f)
            errors = validate_boundary_data(auth_token, boundary_data, "REVENUE")
            if len(errors) > 0:
                print("========================" * 3)
                print("\t" * 8, folder.path.split("/")[-1].upper())
                print("========================" * 3)
                for error in errors:
                    print(error)
                print("\n")


process_boundary(auth_token)
