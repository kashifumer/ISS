import pytz
import requests
from datetime import datetime


MY_LAT = -36.81342669381864
MY_LONG = 174.6003899389404

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()

time_now = datetime.now().strftime('%H')

data = response.json()
sunrise = (data['results']['sunrise'])
sunset = (data['results']['sunset'])


utc_time_str_1 = sunrise
utc_time = datetime.strptime(sunrise, '%Y-%m-%dT%H:%M:%S%z')
auckland_timezone = pytz.timezone('Pacific/Auckland')
auckland_sunrise_time = utc_time.astimezone(auckland_timezone).strftime('%H')

utc_time_str_2 = sunset
utc_time = datetime.strptime(sunset, '%Y-%m-%dT%H:%M:%S%z')
auckland_timezone = pytz.timezone('Pacific/Auckland')
auckland_sunset_time = utc_time.astimezone(auckland_timezone).strftime('%H')


response = requests.get(url='http://api.open-notify.org/iss-now.json')
response.raise_for_status()
data = response.json()

iss_latitude = float(data['iss_position']['latitude'])
iss_longitude = float(data['iss_position']['longitude'])

# is ISS close to my current location


def distance():
    if MY_LAT - iss_latitude <= 5 and MY_LONG - iss_longitude <= 5:
        return "Near"
    else:
        return "far"

# and is it currently dark


def is_dark():
    if auckland_sunrise_time < time_now > auckland_sunset_time:
        return "dark"
    else:
        return "day"


def look_up():
    if distance() == "Near" and is_dark() == "dark":
        return "Look Up!"
    else:
        return "Look Ahead!"


print(look_up())