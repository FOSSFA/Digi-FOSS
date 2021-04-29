import json
import requests
import datetime
import time
import pytz


# A python bot to repost a telegram message that passed one month from first post
# to reread the programming posts

def get_azan(city, day=None):
    data = requests.get('https://api.keybit.ir/owghat', params={'city': city, "day": day})
    json_data = json.loads(data.content)['result']

    azan = json_data['azan_maghreb']
    day = json_data['day']

    return azan, day


cities_code = {'تهران': '1', 'مشهد': '13', 'تبریز': '6', 'قم': '11', 'اصفهان': '2', 'شیراز': '8', 'یزد': '14',
               'ارومیه': '3', 'کرمان': '19', 'اهواز': '5', 'بجنورد': '15', 'گرگان': '18', 'ساری': '17', 'رشت': '16',
               'اردبیل': '26', 'سمنان': '27', 'قزوین': '10', 'زنجان': '25', 'سنندج': '22', 'کرمانشاه': '21',
               'همدان': '24', 'بیرجند': '827', 'ایلام': '29', 'خرم آباد': '30', 'شهرکرد': '31', 'یاسوج': '32',
               'بوشهر': '20', 'زاهدان': '12', 'بندر عباس': '7', 'اراک': '4', 'کرج': '9', 'دزفول': '342',
               'کوالالامپور': '115', 'ساوه': '991', 'شاهرود': '578', 'بروجرد': '479', 'مرند': '450', 'سبزوار': '822',
               'استانبول': '976', 'کیش': '968'}


def get_now():
    TEH = pytz.timezone('Asia/Tehran')
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


# EdgeCase: Last day of month if person ask after azan

def calculate_reminder(city, azan_day=None):
    azan, day = get_azan(city, azan_day)
    now = get_now()
    rH, rM, rS = delta(now, azan, bool(azan_day))
    if rH < 0:
        rH, rM, rS = calculate_reminder(day + 1)
    return rH, rM, rS


if __name__ == "__main__":
    city = "بيرجند"
    print(calculate_reminder(city))

"""
b'{"ok":true,"result":{"azan_sobh":"04:40:50","tolu_aftab":"06:05:12","azan_zohr":"12:33:28","ghorub_aftab":"19:02:16","azan_maghreb":"19:20:12","nimeshab":"23:51:33","month":1,"day":26}}'
"""
