# importing the requests library and environnements and os library
import os
import psycopg2
from dotenv import load_dotenv

# Load environments variables
load_dotenv()

# Connect to the database
connection = psycopg2.connect(
    f"postgres://{str(os.getenv('USERNAME'))}:{str(os.getenv('PASSWORD'))}@postgresql-2791bab0-od486479f.database.cloud.ovh.net:20184/electric?sslmode=require")
cursor = connection.cursor()

# Get the consommation values for each month
cursor.execute(
    "SELECT COUNT(conso) FROM consommation WHERE time > '2022-09-30 23:59:00' AND time < '2022-11-01 00:00:00'")
octobre = cursor.fetchone()
cursor.execute(
    "SELECT COUNT(conso) FROM consommation WHERE time > '2022-10-31 23:59:00' AND time < '2022-12-01 00:00:00'")
novembre = cursor.fetchone()
cursor.execute(
    "SELECT COUNT(conso) FROM consommation WHERE time > '2022-11-30 23:59:00' AND time < '2023-01-01 00:00:00'")
decembre = cursor.fetchone()
print(octobre, novembre, decembre)

# We empty the database
cursor.execute("TRUNCATE conso_month;")

# We add the value of the average in the database
cursor.execute(
    "INSERT INTO conso_month (month,value) VALUES (%s,%s)", ("octobre", octobre))
cursor.execute(
    "INSERT INTO conso_month (month,value) VALUES (%s,%s)", ("novembre", novembre))
cursor.execute(
    "INSERT INTO conso_month (month,value) VALUES (%s,%s)", ("decembre", decembre))

# This is for make the data saved in the database.
connection.commit()

# Close the database
cursor.close()
connection.close()
