import requests
import json


"""
Informations used by the API
"""
API_HOST = 'cityscoot.eu'
APP_VERSION = '3.2.3'
APP_DEVICE_UDID = 'a4fa79c5f9682471'
APP_FLYER_ID = '1654072922843-4881979020824136565'

DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = '9'
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_CLIENT = 'okhttp/3.9.1'


"""
Send a request to the API
"""
def request(endpoint, api='publicapi'):
    # build the headers
    headers = {
        'Host': f'{api}.{API_HOST}',
        'X-Device-Udid': APP_DEVICE_UDID,
        'X-Device-Material': DEVICE_NAME,
        'X-Device-Os': DEVICE_OS_NAME,
        'X-Device-Os-Version': DEVICE_OS_VERSION,
        'X-Application-Version': APP_VERSION,
        'X-Device-Locale': f'{DEVICE_LANG}-{DEVICE_REGION}',
        'X-Appsflyer-Id': APP_FLYER_ID,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': APP_CLIENT
    }

    # send the request
    response = requests.get(f'https://{api}.{API_HOST}/{endpoint}', headers=headers)

    # return the response
    return response

"""
Get the zones list
"""
def get_zones():
    # request the zones list
    response = request('api/v1/city?', api='api-v3')

    # check the response status code
    if response.status_code != 200:
        print('Error: Cityscoot: get_zones: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)

"""
Get the shared vehicles list
"""
def get_vehicles(zone_id=None):
    # TODO: if no zone_id get all the zones and all the vehicles from all zones
    # request the vehicles list
    response = request(f'api/scooters/public/city/{zone_id}?')

    # check the response status code
    if response.status_code != 200:
        print('Error: Cityscoot: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
