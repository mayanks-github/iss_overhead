import datetime
import smtplib
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

Email_id = os.getenv('id')
Password = os.getenv('new_key')
Receiver_email = os.getenv('receiver_email')

MY_LAT = '22.91694560367614',
My_LNG = '75.85903168029628'
parameter = {
    "lat": MY_LAT,
    'lng': My_LNG,
    'formatted': 0,
}


def is_iss_overhead():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    data_iss = response_iss.json()
    longitude = float(data_iss['iss_position']['longitude'])
    latitude = float(data_iss['iss_position']['latitude'])
    iss_position = (longitude, latitude)
    if float(My_LNG) + 5 >= iss_position[1] >= float(My_LNG) - 5 and float(MY_LAT) + 5 >= iss_position[2] >= float(
            MY_LAT) - 5:
        return True


def is_night():
    response_time = requests.get(f'https://api.sunrise-sunset.org/json', params=parameter)
    response_time.raise_for_status()
    data_time = response_time.json()
    sunrise = int(data_time['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data_time['results']['sunset'].split("T")[1].split(":")[0])
    right_now = datetime.datetime.now().hour

    if right_now >= sunset or right_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=Email_id, password=Password)
            connection.sendmail(from_addr=Email_id, to_addrs=Receiver_email,
                                msg=f"Subject:Look Up\n\nISS is over head. You can check it out.")
