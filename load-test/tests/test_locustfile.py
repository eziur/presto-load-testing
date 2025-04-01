import random
import pytest

lat_min, lat_max = 32.8182, 33.5051
lon_min, lon_max = -117.2433, -116.0806

def generate_rzrisk_payload():

    payload = {
      "location": {
        "latitude": 33.022889,
        "longitude": -117.143715
      },
    }

    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    payload['location']['latitude'] = lat
    payload['location']['longitude'] = lon
    return payload['location']['latitude'], payload['location']['longitude']

def test_generate_rzrisk_payload():
    lat, lon = generate_rzrisk_payload()
    assert lat_min <= lat <= lat_max
    assert lon_min <= lon <= lon_max