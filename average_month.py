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

# We empty the database
cursor.execute("TRUNCATE conso_month;")

# Tab with all the months
month = ["janvier", "fevrier", "mars", "avril", "mai", "juin",
         "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]


# Add the value of conso for each month in the postgreSQL table
for i in range(1, 13):
    # Define the start and end value for each month
    if (i == 1) or (i == 3) or (i == 5) or (i == 7) or (i == 8):
        start = f'2023-0{i}-01 00:00:00'
        end = f"2023-0{i}-31 00:00:00"
    if (i == 10) or (i == 12):
        start = f'2022-{i}-01 00:00:00'
        end = f"2022-{i}-31 00:00:00"
    if (i == 2):
        start = f'2023-0{i}-01 00:00:00'
        end = f"2023-0{i}-28 00:00:00"
    if (i == 4) or (i == 6) or (i == 9):
        start = f'2023-0{i}-01 00:00:00'
        end = f"2023-0{i}-30 00:00:00"
    if i == 11:
        start = f'2022-{i}-01 00:00:00'
        end = f"2022-{i}-30 00:00:00"
    # Get from the database the conut of the month
    cursor.execute(
        f"SELECT SUM(conso) FROM consommation WHERE time >= '{start}' AND time < '{end}'")
    value = cursor.fetchone()
    # We insert the value of the month in the database.
    cursor.execute(
        f"INSERT INTO conso_month (month,value) VALUES (%s,%s)", (month[i-1], value))

# This is for make the data saved in the database.
connection.commit()

# Close the database
cursor.close()
connection.close()
