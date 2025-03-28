import logging
import os
import random
import json
import locust.stats
from locust import HttpUser, task, between, events

RZLT_ORG = os.getenv('RZLT_ORG', 'RZADMIN0')
RZLT_API_TOKEN = os.getenv('RZLT_API_TOKEN')

locust.stats.CSV_STATS_INTERVAL_SEC = 10 # logging interval

def generate_random_location():
    lat_min, lat_max = 32.5343, 33.5051
    lon_min, lon_max = -117.2825, -116.0806

    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)

    return lat, lon

def generate_rzrisk_payload():
    payload = {
      "metadata": {
        "requestTag": "locust",
        "units": {
          "distance": "miles"
        }
      },
      "location": {
        "address": "8127 Silverwind Dr",
        "city": "San Diego",
        "state": "CA",
        "zip": "92127",
        "latitude": 33.022889,
        "longitude": -117.143715
      },
      "rzFeatures": {
        "insightScoring": {
          "constructionType": 0,
          "noncombustibleVerticalClearance": 0,
          "defensibleZone2": 0,
          "defensibleZone1": 1,
          "roofType": 1,
          "enclosedEaves": 1,
          "wildfirePreparedCommunity": 0,
          "yearBuilt": 0,
          "fireResistiveVents": 1,
          "wildfireMitigationCertification": 0,
          "occupancyType": 1,
          "exteriorMaterial": 0,
          "defensibleZone3": 0,
          "woodDeck": 0,
          "windowPaneType": 1
        },
        "correlatedRiskZones": True,
        "averageAnnualLoss": {
          "siteDeductibleAsPctOfTotal": 10,
          "totalInsuredValue": 4000000
        },
        "firewiseCommunity": True,
        "distanceToHigherRiskClasses": True,
        "activeFires": True,
        "riskScoring": True,
        "fireHistory": True,
        "fireRiskReductionCommunity": True
      }
    }

    lat, lon = generate_random_location()
    payload['location']['latitude'] = lat
    payload['location']['longitude'] = lon
    return payload

class User(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + RZLT_API_TOKEN,
            "Content-Type": "application/json",
        }

    @task
    def test_rzrisk(self):
        payload = generate_rzrisk_payload()

        with self.client.post(
            url='/api/v1/' + RZLT_ORG + '/rzrisk',
            data=json.dumps(payload),
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Request failed! Status: {response.status_code}, Response: {response.text}")

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

if __name__ == "__main__":
    import os
    os.system("locust")