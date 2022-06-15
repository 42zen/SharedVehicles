import requests
import json


"""
Informations used by the API
"""
API_HOST = 'platform.api.gourban.services'

DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = 9
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_NAME = 'greenmo'
APP_VERSION = '1.2.46'
APP_CLIENT = f'{APP_NAME}/{APP_VERSION};{DEVICE_OS_NAME}/{DEVICE_OS_VERSION};{DEVICE_NAME}'


"""
Get the shared vehicles list
"""
def get_vehicles(lat, lng, radius=0.9313955833990112):
    # build the headers
    headers = {
        'Host': API_HOST,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION}',
        'User-Agent': APP_CLIENT,
        'Os': DEVICE_OS_NAME,
        'Device-Position': f'{lat};{lng}',
        'App-Version': APP_VERSION
    }

    # build the params
    params = {
        'lat': lat,
        'lng': lng,
        'rad': radius
    }

    # send the request
    response = requests.get(f'https://{API_HOST}/v1/greenmo/front/vehicles', params=params, headers=headers)

    # check the response status code
    if response.status_code != 200:
        print('Error: GoSharing: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
