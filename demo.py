# importing the requests library and environnements and os library
import os

# Import the library for the database.
import psycopg2

# Import the library to read the json.
import json

# Import library for the environment
from dotenv import load_dotenv

# Load environments variables
load_dotenv()

# Open the value in the json file
with open("demo.json") as f:
    data = json.load(f)


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
        try:
            cursor.execute(
                "INSERT INTO consommation (time,conso,is_heures_pleines) VALUES (%s,%s,%s); ", (date, value, 0))
        except Exception:
            pass
    else:
        try:
            cursor.execute(
                "INSERT INTO consommation (time,conso,is_heures_pleines) VALUES (%s,%s,%s); ", (date, value, 1))
        except Exception:
            pass

# This is for make the data saved in the database.
connection.commit()

# Close the database
cursor.close()
connection.close()
