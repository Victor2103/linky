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
URL = f"https://www.myelectricaldata.fr/daily_consumption/{str(os.getenv('PDL'))}/start/2022-09-05/end/2022-10-12"
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
    os.getenv('PDL')), "start": "2022-12-20", "end": "2022-12-31"}
# sending post request and saving the response as response object
r = requests.post(url=URL, headers=PARAMS, data=json.dumps(data))
# extracting data in json format
data = r.json()


# print(data)
print(data["meter_reading"]["interval_reading"][0]["value"])
print(data["meter_reading"]["interval_reading"][0]["date"])


# Connect to the database
connection = psycopg2.connect(
    f"postgres://{str(os.getenv('USERNAME'))}:{str(os.getenv('PASSWORD'))}@postgresql-2791bab0-od486479f.database.cloud.ovh.net:20184/electric?sslmode=require")
cursor = connection.cursor()

# Make a query inside the database
# cursor.execute("")
# cursor.fetchone()

# Close the database
cursor.close()
connection.close()
