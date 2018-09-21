import traceback

import create_employee_script
import fireCessGen
from config import config, load_config

import PTBoundaryGen
import departmentGen
import designationGen
import tenantGen
import employeeGen
from processing import PTDBScript

cities = ["Alawalpur"]
cities = ["Dasuya", "Handiaya", "Lalru", "Shahkot", "SultanpurLodhi", "Adampur", "Alawalpur", "Arniwala", "BassiPathana", "Bhogpur", "Dasuya", "Dharamkot", "Garhshankar", "Hariana", "Khanauri", "LohianKhas", "Mahilpur", "Makhu", "Mallanwala", "Mudki", "ShamChurasi", "Sunam", "Talwara", "Tapa", "UrmarTanda", "Zirakpur"]

cities = ["Shahkot", "Handiaya", "Lalru", "Dasuya", "Sultanpur Lodhi", "Zirakpur"]

# cities = ["Testing"]

cities = ["Sultanpur Lodhi"]

for city in cities[:]:
    try:
        config.CITY_NAME = city.replace(" ", "")
        load_config()

        step = "Generating Employee data"
        print(step)
        employeeGen.main()

        # create_employee_script.main()
        step = "Generating tenant data"
        print(step)
        tenantGen.main()

        step = "Generating firecess config"
        print(step)
        fireCessGen.main()

        step = "Generating department data"
        print(step)
        departmentGen.main()

        step = "Generating designation data"
        print(step)
        designationGen.main()

        step = "Generating Boundary data"
        print(step)
        PTBoundaryGen.main()

        step = "Generating SQL data"
        print(step)
        PTDBScript.main()
    except Exception as ex:
        print("City", city, "failed", step, str(ex))
        traceback.print_exc()