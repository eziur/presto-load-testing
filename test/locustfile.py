import logging
import os
import random
import json
import locust.stats
from locust import HttpUser, task, between, events

ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging')
USER = os.getenv('USER', 'RZADMIN0')
DATA = os.getenv('DATA')
TOKEN = os.getenv('TOKEN')

locust.stats.CSV_STATS_INTERVAL_SEC = 1 # logging interval

def generate_random_location():
    lat_min, lat_max = 32.5343, 33.5051
    lon_min, lon_max = -117.2825, -116.0806

    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)

    return lat, lon

class User(HttpUser):
    wait_time = between(1, 1)

    @task
    def temp(self):
        lat, lon = generate_random_location()

        with open('rzrisk.json', 'r') as f:
            payload = json.load(f)

        payload['location']['latitude'] = lat
        payload['location']['longitude'] = lon

        payload = json.dumps(payload)

        self.client.post(
            url='https://risk.' + ENVIRONMENT + '.redzone.zone/api/v1/' + USER + '/rzrisk/',
            data=payload,
            auth=None,
            headers={
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + TOKEN,
                'Content-Type': 'application/json'},
        )

    @events.quitting.add_listener
    def _(environment, **kw):
        if environment.stats.total.fail_ratio > 0.25:
            logging.error('Test failed due to failure ratio > 25%')
            environment.process_exit_code = 1
        elif environment.stats.total.avg_response_time > 1000:
            logging.error('Test failed due to average response time ratio > 1000 ms')
            environment.process_exit_code = 1
        elif environment.stats.total.get_response_time_percentile(0.95) > 2000:
            logging.error('Test failed due to 95th percentile response time > 2000 ms')
            environment.process_exit_code = 1
        else:
            environment.process_exit_code = 0

