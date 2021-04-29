import json
import requests
import datetime
import time
import pytz
import logging
from enum import Enum

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


class AzanTypes(Enum):
    Maghrib = 'Maghrib'


def get_azan(city, timestamp=None, azan_type=AzanTypes.Maghrib):
    timestamp_text = f"/{timestamp}" if not timestamp is None else ""
    url = f"http://api.aladhan.com/v1/timingsByAddress" + timestamp_text
    try:
        data = requests.get(url, params={"address": city, "method": 7})
        json_data = json.loads(data.content)['data']

        azan = json_data['timings'][azan_type.value]
        timezone = json_data['meta']['timezone']
        timestamp = json_data['date']['timestamp']
    except Exception as e:
        print('Exception, ', e)
        return None, None, None

    return azan, timezone, int(timestamp)


def get_now(timezone):
    TEH = pytz.timezone(timezone)
    now = datetime.datetime.now(TEH)
    now_text = str(now).split(' ')[-1].split('.')[0]

    return now_text


def delta(time1, time2, fix_hour):
    h1, m1, s1 = [int(i) for i in time1.split(":")]
    h2, m2, s2 = [int(i) for i in time2.split(":")]
    h, m, s = h2 - h1, m2 - m1, s2 - s1

    if s < 0:
        s += 60
        m -= 1

    if m < 0:
        m += 60
        h -= 1

    if fix_hour and h < 0:
        h += 24

    return (h, m, s)


def calculate_reminder(city, new_timestamp=None):
    azan, timezone, timestamp = get_azan(city, timestamp=new_timestamp)
    if azan is None:
        return None, None, None
    azan += ":00"
    now = get_now(timezone)

    rH, rM, rS = delta(now, azan, bool(new_timestamp))

    logger.debug(f"Now: {now} Azan is: {azan} >> {rH}:{rM}:{rS}")
    if rH < 0:
        rH, rM, rS = calculate_reminder(city, new_timestamp=timestamp + (24 * 60 * 60))
    return rH, rM, rS


if __name__ == "__main__":
    city = "چين"
    ch.setLevel(logging.DEBUG)
    print(calculate_reminder(city))

"""
b'{"ok":true,"result":{"azan_sobh":"04:40:50","tolu_aftab":"06:05:12","azan_zohr":"12:33:28","ghorub_aftab":"19:02:16","azan_maghreb":"19:20:12","nimeshab":"23:51:33","month":1,"day":26}}'
"""
