import requests
from constants import URL_TEST_LIB


def get_test_lib():
    with open('utils/testlib.h', 'r') as file:
        data = file.read()
    return data


def get_test_lib_official():
    response = requests.get(URL_TEST_LIB, stream=True)
    response.raise_for_status()
    response.raw.decode_content = True
    return response.text
