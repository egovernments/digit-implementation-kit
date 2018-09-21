from os import path
import os
from shutil import copyfile

for f in os.scandir("/Users/tarunlalwani/Downloads/PT-Final Data for Roll-out/Data/Other ULBs Data_without Fire Cess"):
    if path.isdir(f.path):
        tenant_id = f.name.replace(" ","").lower()
        new_path = "../logos/pb.{}".format(tenant_id)
        os.makedirs(new_path, exist_ok=True)
        print("Processing " + f.name)

        for f2 in os.scandir(f.path):
            if path.isfile(f2) and f2.name.lower().endswith("png"):
                print("Logo found")
                copyfile(f2.path, "{}/logo.png".format(new_path))

            if path.isfile(f2) and f2.name.lower().endswith("xlsx"):
                print("Source sheet found")
                copyfile(f2.path, "../source/{}.xlsx".format(tenant_id))
