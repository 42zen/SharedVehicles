import requests
import json


"""
Informations used by the API
"""
API_HOST = 'maps.nextbike.net'
API_KEY = 'rXXqTgQZUPZ89lzB'

DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_CONSTRUCTOR = 'Google'

APP_NAME = 'nextbike'
APP_VERSION = 'a.v4-v4.12.16'


"""
Send a request to the API
"""
def _request(endpoint):
    # build the headers
    headers = {
        'Host': API_HOST,
        'User-Agent': f'{APP_NAME}/{APP_VERSION}/{DEVICE_CONSTRUCTOR} {DEVICE_NAME}'
    }

    # build the params
    params = {
        'api_key': API_KEY
    }

    # send the request
    response = requests.get(f'https://{API_HOST}/{endpoint}', params=params, headers=headers)

    # return the response
    return response

"""
Get the shared vehicles list for a zone
"""
def get_vehicles():
    # send the request
    response = _request('maps/nextbike-live.flatjson')

    # check the response status code
    if response.status_code != 200:
        print('Error: NextBike: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
