import requests
import json


"""
Informations used by the API
"""
API_HOST = 'vehicles.linkyour.city'
APP_NAME = 'LINK'
APP_VERSION = '5.0.7'
APP_BUILD_VERSION = '4477'
APP_DEVICE_KEY = '34d302b0-6e80-4387-98ee-b0a1086b3295'

DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_CONSTRUCTOR = 'Google'
DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = 9
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_CLIENT = f'{DEVICE_OS_NAME}/{DEVICE_OS_VERSION} {APP_NAME}/{APP_VERSION}/{APP_BUILD_VERSION}'
APP_DEVICE = f'{APP_DEVICE_KEY}/{DEVICE_CONSTRUCTOR}/{DEVICE_NAME}'


"""
Send a request to the API
"""
def _request(endpoint, params=None):
    # build the headers
    headers = {
        'Host': API_HOST,
        'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION}',
        'User-Agent': APP_CLIENT,
        'User-Device': APP_DEVICE,
        'Connection': 'close'
    }

    # send the request
    response = requests.get(f'https://{API_HOST}/{endpoint}', params=params, headers=headers)

    # return the response
    return response

"""
Get the shared vehicles list
"""
def get_vehicles(lat, lng):
    # build the params
    params = {
        'latitude': lat,
        'longitude': lng
    }

    # send the request
    response = _request('reservation-api/local-vehicles/', params=params)

    # check the response status code
    if response.status_code != 200:
        print('Error: Superpedestrian: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
