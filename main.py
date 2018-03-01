import requests
import schedule
import time
from config import config


def get_aqi():
    return requests.get("http://api.waqi.info/feed/geo:39.913818;116.363625/?token=%s" %
                        config.token)


def trigger_ifttt(event, value1="", value2="", value3="", ):
    requests.post(
        "https://maker.ifttt.com/trigger/%s/with/key/%s" % (event, config.ifttt_token),
        json={
            "value1": value1,
            "value2": value2,
            "value3": value3
        })


def trigger_ifttt_if_aqi_is_bad():
    response = get_aqi()
    pm25 = response.json()['data']['iaqi']['pm25']['v']
    pm25_threshold = 60
    if pm25 > pm25_threshold:
        event = "aqicn"
        trigger_ifttt(event, pm25)
    print(response.text)


if __name__ == '__main__':
    schedule.every().days.at("7:30").do(trigger_ifttt_if_aqi_is_bad)
    schedule.every().days.at("18:00").do(trigger_ifttt_if_aqi_is_bad)
    while True:
        schedule.run_pending()
        time.sleep(100)
