# importing the requests library and environnements and os library
import requests
from dotenv import load_dotenv
import os
import psycopg2

# Load environments variables
load_dotenv()

# api-endpoint
URL = f"https://www.myelectricaldata.fr/daily_consumption_max_power/{str(os.getenv('PDL'))}/start/2022-09-05/end/2022-10-12"
# defining a params dict for the parameters to be sent to the API
PARAMS = {"Authorization": str(os.getenv("TOKEN"))}
# sending get request and saving the response as response object
r = requests.get(url=URL, headers=PARAMS)
# extracting data in json format
data = r.json()

print(data["meter_reading"]["interval_reading"][0])


#Connect to the database
connection=psycopg2.connect(f"postgres://{str(os.getenv('USERNAME'))}:{str(os.getenv('PASSWORD'))}@postgresql-2791bab0-od486479f.database.cloud.ovh.net:20184/electric?sslmode=require")
cursor = connection.cursor()

# Make a query inside the database
#cursor.execute("")
#cursor.fetchone()

#Close the database
cursor.close()
connection.close()