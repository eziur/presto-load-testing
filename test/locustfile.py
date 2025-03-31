import json
import locust.stats
import os
import random
from locust import HttpUser, task, between, events


RZLT_ORG = os.getenv('RZLT_ORG', 'RZADMIN0')
RZLT_API_TOKEN = os.getenv('RZLT_API_TOKEN')


locust.stats.CSV_STATS_INTERVAL_SEC = 10 # logging interval

def generate_rzrisk_payload():
    lat_min, lat_max = 32.5343, 33.5051
    lon_min, lon_max = -117.2825, -116.0806
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

    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    payload['location']['latitude'] = lat
    payload['location']['longitude'] = lon
    return payload


class RedZoneAPIUser(HttpUser):
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
        with self.client.post('/api/v1/' + RZLT_ORG + '/rzrisk', data=json.dumps(payload), catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Request failed! Status: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    import os
    os.system("locust")