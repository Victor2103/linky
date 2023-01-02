# importing the requests library and environnements and os library
import requests
from dotenv import load_dotenv
import os
import psycopg2
import json

# Load environments variables
load_dotenv()

"""
# api-endpoint for my electrical data
URL = f"https://www.myelectricaldata.fr/daily_consumption/{str(os.getenv('PDL'))}/start/2022-12-29/end/2022-12-31"
# defining a params dict for the parameters to be sent to the API
PARAMS = {"Authorization": str(os.getenv("TOKEN"))}
# sending get request and saving the response as response object
r = requests.get(url=URL, headers=PARAMS)
# extracting data in json format
data = r.json()
"""

# api-endpoint for enedis gateway
URL = "https://enedisgateway.tech/api"
# Defining the headers
PARAMS = {'Authorization': str(
    os.getenv("ENEDIS_TOKEN")), 'Content-Type': "application/json"}
# Defining the data to post
data = {"type": "daily_consumption", "usage_point_id": str(
    os.getenv('PDL')), "start": "2022-12-29", "end": "2022-12-31"}
# sending post request and saving the response as response object
r = requests.post(url=URL, headers=PARAMS, data=json.dumps(data))
# extracting data in json format
data = r.json()

print(data)
# print(data["meter_reading"]["interval_reading"][0]["value"])
# print(data["meter_reading"]["interval_reading"][0]["date"])

# Connect to the database
connection = psycopg2.connect(
    f"postgres://{str(os.getenv('USERNAME'))}:{str(os.getenv('PASSWORD'))}@postgresql-2791bab0-od486479f.database.cloud.ovh.net:20184/electric?sslmode=require")
cursor = connection.cursor()

# We make a loop and we save all the data in the database
for i in range(0, len(data["meter_reading"]["interval_reading"])):
    date = data["meter_reading"]["interval_reading"][i]["date"]
    value = data["meter_reading"]["interval_reading"][i]["value"]
    # Make a query inside the database and save the value of the consommation
    cursor.execute(
        "INSERT INTO production_real_time (time,value) VALUES (%s,%s); ", (date, value))


# Make a query inside the database and save one value of the electricity
cursor.execute(
    "INSERT INTO production_real_time (time,value) VALUES (%s,%s); ", (date, value))

# Show if the query has worked
cursor.execute("SELECT * FROM production_real_time ;")
# Use fettch one to print only the value you add
print(cursor.fetchone())

"""
# This is for make the data saved in the database. 
connection.commit()
"""

# Close the database
cursor.close()
connection.close()
