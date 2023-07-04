import smtplib
import time

import requests
from datetime import datetime

LATITUDE = 18.520430
LONGITUDE = 73.856743
EMAIL = "A@gmail.com"
PWD = "hopperinsand"

def is_detected():
    data = requests.get(url="http://api.open-notify.org/iss-now.json")
    data.raise_for_status()
    info = data.json()

    iss_lati = float(info["iss_position"]["latitude"])
    iss_longi = float(info["iss_position"]["longitude"])

    if LATITUDE - 5 <= iss_lati <= LATITUDE + 5 and LONGITUDE - 5 <= iss_longi <= LATITUDE + 5:
        return True


def check_nighttime():
    parameters = {
        "lat": LONGITUDE,
        "lng": LONGITUDE,
        "formatted": 0
    }

    data = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    data.raise_for_status()
    info = data.json()

    sunrise = int(info["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(info["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour #returning in hour time

    #checking darkness time
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(100)
    if is_detected() and check_nighttime():
        with smtplib.SMTP("smtp.google.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PWD)
            connection.sendmail(to_addrs="mac@gmail.com", from_addr=EMAIL, msg="Subject: ISS Detected Over Your Location \n\n Your current longitude and latitude are similar to ISS, LOOK Up in the SKY!")




