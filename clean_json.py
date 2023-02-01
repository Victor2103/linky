# importing the requests library and environnements and os library
import os
import psycopg2
import json
from dotenv import load_dotenv

# Load environments variables
load_dotenv()


# Definition of the function who add the data in the database
def add_into_heures_creuses(nameFile):
    with open(nameFile) as f:
        data = json.load(f)

    # Test if the json is correctly load
    # print(data)
    print(data["meter_reading"]["interval_reading"][23]["value"])

    # Connect to the database
    connection = psycopg2.connect(
        f"postgres://{str(os.getenv('USERNAME'))}:{str(os.getenv('PASSWORD'))}@postgresql-2791bab0-od486479f.database.cloud.ovh.net:20184/electric?sslmode=require")
    cursor = connection.cursor()
