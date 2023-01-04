# importing the requests library and environnements and os library
import requests
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

    # We make a loop and we save all the data in the database
    for i in range(0, len(data["meter_reading"]["interval_reading"])):
        date = data["meter_reading"]["interval_reading"][i]["date"]
        value = data["meter_reading"]["interval_reading"][i]["value"]
        hour = date.split(" ")[1]
        hour_clean = int(hour[0]+hour[1]+hour[3]+hour[4])
        # Check if we make the query (we are in empty hours)
        if (hour_clean > 6 and hour_clean < 736) or (hour_clean > 1236 and hour_clean < 1336):
            # Make a query inside the database and save the value of the consommation
            cursor.execute(
                "INSERT INTO heures_creuses (time,heures_creuses) VALUES (%s,%s); ", (date, value))
        else:
            cursor.execute(
                "INSERT INTO heures_pleines (time,heures_pleines) VALUES (%s,%s); ", (date, value))

    # Show if the query has worked
    cursor.execute("SELECT * FROM heures_creuses ;")
    # Use fettch one to print only the value you add
    print(cursor.fetchone())

    # This is for make the data saved in the database.
    connection.commit()

    # Close the database
    cursor.close()
    connection.close()


# For each data in the json, we add into our database on the public cloud.
for i in range(2, 15):
    add_into_heures_creuses(f"my_data/appel_{i}.json")
    print(f"File appel_{i}.json added ! ")
