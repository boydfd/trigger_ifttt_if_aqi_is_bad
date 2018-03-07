import time
from _socket import timeout

import requests
import schedule

from config import config
from user_config import UserConfig
from utilities import retry_for_exception_decorator


def get_aqi():
    return requests.get("http://api.waqi.info/feed/geo:39.913818;116.363625/?token=%s" %
                        config['token'])


def trigger_ifttt(event, ifttt_token, value1="", value2="", value3="", ):
    requests.post(
        "https://maker.ifttt.com/trigger/%s/with/key/%s" % (event, ifttt_token),
        json={
            "value1": value1,
            "value2": value2,
            "value3": value3
        })


@retry_for_exception_decorator(timeout)
def trigger_ifttt_if_aqi_is_bad(user_config: UserConfig):
    response = get_aqi()
    pm25 = response.json()['data']['iaqi']['pm25']['v']
    if pm25 > user_config.pm25_threshold:
        event = "aqicn"
        trigger_ifttt(event, user_config.ifttt_token, pm25, )
    print(response.text)


def schedule_for_user(user_config: UserConfig):
    for t in user_config.times:
        schedule.every().days.at(t).do(
            lambda: trigger_ifttt_if_aqi_is_bad(user_config))


if __name__ == '__main__':
    for user in config['ifttt_users'].values():
        schedule_for_user(user)
    # schedule.every().days.at("7:30").do(trigger_ifttt_if_aqi_is_bad)
    # schedule.every().days.at("18:00").do(trigger_ifttt_if_aqi_is_bad)
    while True:
        schedule.run_pending()
        time.sleep(10)
