from load_test import constants, locustfile

def test_generate_coordinates():
    payload = locustfile.generate_rzrisk_payload()
    lat, lon = payload['location']['latitude'], payload['location']['longitude']
    assert constants.LAT_MIN <= lat <= constants.LAT_MAX, f"Latitude {lat} out of bounds"
    assert constants.LON_MIN <= lon <= constants.LON_MAX, f"Longitude {lon} out of bounds"