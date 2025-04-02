import pytest

pytest_plugins = [
    "load_test.locustfile"
]

lat_min, lat_max = 32.8182, 33.5051
lon_min, lon_max = -117.2433, -116.0806

def test_generate_rzrisk_payload(generate_payload):
    lat, lon = generate_payload
    assert lat_min <= lat <= lat_max
    assert lon_min <= lon <= lon_max