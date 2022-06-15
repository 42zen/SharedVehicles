import requests
import json


"""
Informations used by the API
"""
API_HOST = 'api.zeus.cooltra.com'
API_TOKEN = 'Bearer 77b78f223d8efc78cd3b31c587cd9276413d214234047766881042eb1ca637ba'

DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_CONSTRUCTOR = 'Google'
DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = 9

APP_NAME = 'Cooltra'
APP_VERSION = '4.6.4'
APP_PACKAGE_NAME = 'com.mobime.ecooltra'
APP_PACKAGE_BUILD = 470
APP_CLIENT = f'{APP_NAME}/{APP_VERSION} ({APP_PACKAGE_NAME}; build:{APP_PACKAGE_BUILD}; {DEVICE_OS_NAME} {DEVICE_OS_VERSION}; {DEVICE_CONSTRUCTOR} {DEVICE_NAME})'


"""
Send a request to the API
"""
def _request(endpoint):
    # build the headers
    headers = {
        'Host': API_HOST,
        'Authorization': API_TOKEN,
        'User-Agent': APP_CLIENT
    }

    # send the request
    return requests.get(f'https://{API_HOST}/mobile_cooltra/v1/{endpoint}', headers=headers)

"""
Get the current configuration
"""
def get_configuration():
    # send the request
    response = _request('configuration')

    # check the response status code
    if response.status_code != 200:
        print('Error: Cooltra: get_zones: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)

"""
Get the shared vehicles list for a zone
"""
def get_vehicles(zone):
    # send the request
    response = _request(f'vehicles?system_id={zone}')

    # check the response status code
    if response.status_code != 200:
        print('Error: Cooltra: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
