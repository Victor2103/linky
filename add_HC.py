# importing the requests library and environnements and os library
import os
import psycopg2
import json
from dotenv import load_dotenv
import requests

# Load environments variables
load_dotenv()

# Function who define the message to send to telegram


def telegram_bot_sendtext(bot_message):

    bot_token = str(os.getenv('API_TELEGRAM'))
    bot_chatID = str(os.getenv('CHAT_ID'))
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


# Definition of the function who add the data in the database
def add_into_heures_creuses(nameFile):
    with open(nameFile) as f:
        data = json.load(f)

    # Connect to the database
    connection = psycopg2.connect(
        f"postgres://{str(os.getenv('USERNAME'))}:{str(os.getenv('PASSWORD'))}@postgresql-2791bab0-od486479f.database.cloud.ovh.net:20184/electric?sslmode=require")
    cursor = connection.cursor()

    # For each value we add it into the database.
    for i in range(0, len(data["meter_reading"]["interval_reading"])):
        # We get the value of the date and the consommation to add
        date = data["meter_reading"]["interval_reading"][i]["date"]
        value = data["meter_reading"]["interval_reading"][i]["value"]
        # We check if the value is already in the database
        cursor.execute(
            f"SELECT exists (SELECT time FROM consommation WHERE time = '{date}' LIMIT 1);")
        result = cursor.fetchone()
        # If the value is not present in the database we added it in the db.
        if result[0] == False:
            hour = date.split(" ")[1]
            hour_clean = int(hour[0]+hour[1]+hour[3]+hour[4])
            # Check the difference with off-peak hours and non off peak hours.
            if (hour_clean > 6 and hour_clean < 736) or (hour_clean > 1236 and hour_clean < 1336):
                cursor.execute(
                    "INSERT INTO consommation (time,conso,is_heures_pleines) VALUES (%s,%s,%s); ", (date, value, 0))
            else:
                cursor.execute(
                    "INSERT INTO consommation (time,conso,is_heures_pleines) VALUES (%s,%s,%s); ", (date, value, 1))

    # This is for make the data saved in the database.
    connection.commit()

    # Close the database
    cursor.close()
    connection.close()

    # Send a message to telegram
    telegram_bot_sendtext("Well done, your data has been added ! ")


# For each data in the json, we add into our database on the public cloud.
for i in range(31, 32):
    add_into_heures_creuses(f"my_data/appel_{i}.json")
    print(f"File appel_{i}.json added ! ")


"""
add_into_heures_creuses("my_data/appel_15.json")
add_into_heures_creuses("my_data/appel_16.json")
"""
