import requests
from datetime import datetime
from smtplib import SMTP
import time

MY_EMAIL = "darksnake0101@gmail.com"
PASSWORD = "'hreyelognhxkndcn"

MY_LAT = -23.771666
MY_LONG = -46.590491

def position_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])
    if MY_LONG-5 <= iss_longitude <= MY_LONG+5 and MY_LAT-5 <= iss_latitude <= MY_LAT+5:
        return True
    
def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0
    }

    response = requests.get('https://api.sunrise-sunset.org/json',params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    
    time_now = datetime.now().hour
    
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if position_overhead() and is_night():
        with SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs='alyssonassissantos@gmail.com',
                msg='Subject:Look Up\n\n O ISS está sobre sua cabeça e pode ser visivel.'
            )
    
    