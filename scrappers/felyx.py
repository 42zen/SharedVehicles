import requests
import json


"""
Informations used by the API
"""
API_HOST = 'relay.felyx.com'

DEVICE_OS_NAME = 'Android'
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_NAME = 'Felyx'
APP_VERSION = '1.4.0-10004000'
APP_PACKAGE_NAME = 'com.felyx.android'
APP_CLIENT = f'{APP_NAME} {DEVICE_OS_NAME}/{APP_VERSION}'


"""
Get the shared vehicles list
"""
def get_vehicles(lat, lng, radius=0.08426981046):
    # build the headers
    headers = {
        'Host': API_HOST,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': APP_CLIENT,
        'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION}',
        'X-Appid': APP_PACKAGE_NAME
    }

    # build the params
    params = {
        'lat1': lat + radius,
        'lon1': lng + radius,
        'lat2': lat - radius,
        'lon2': lng - radius
    }

    # send the request
    response = requests.get(f'https://{API_HOST}/map/cars', params=params, headers=headers)

    # check the response status code
    if response.status_code != 200:
        print('Error: Felyx: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
