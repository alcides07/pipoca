import requests
from constants import URL_TEST_LIB


def get_test_lib():
    response = requests.get(URL_TEST_LIB, stream=True)
    response.raise_for_status()
    response.raw.decode_content = True
    return response.text
