from datetime import datetime

given_date = "8-6-2022"
formated_date = datetime.strptime(given_date,"%d-%m-%Y")
Unix_timestamp = int(datetime.timestamp(formated_date)*1000)
print("The Unix timestamp for the given input date is:")
print(Unix_timestamp)