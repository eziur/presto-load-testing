from load_test.src.locustfile import generate_rzrisk_payload
from load_test.src import constants

def test_generate_coordinates():
    payload = generate_rzrisk_payload()
    lat, lon = payload['location']['latitude'], payload['location']['longitude']
    assert constants.LAT_MIN <= lat <= constants.LAT_MAX, f"Latitude {lat} out of bounds"
    assert constants.LON_MIN <= lon <= constants.LON_MAX, f"Longitude {lon} out of bounds"