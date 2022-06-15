import requests
import json


"""
Informations used by the API
"""
API_HOST = 'api.jcdecaux.com'
API_TOKEN = 'eec049588f516157d84d12edb645b254feb1bdc6'
API_ID = '1653337444566'

DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_OS_NAME = 'Android'
DEVICE_OS_ORIGIN = 'Linux'
DEVICE_OS_VERSION = 9
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_PACKAGE_NAME = 'com.altairapps.villo'
APP_CLIENT = f'Mozilla/5.0 ({DEVICE_OS_ORIGIN}; {DEVICE_OS_NAME} {DEVICE_OS_VERSION}; {DEVICE_NAME} Build/PSR1.180720.122; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36'

# TODO: get_zones

"""
Get the shared vehicles list
"""
def get_vehicles(zone='bruxelles'):
    # build the headers
    headers = {
        'Host': API_HOST,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': APP_CLIENT,
        'Content-Type': 'application/json',
        'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION}',
        'X-Requested-With': APP_PACKAGE_NAME,
        'Connection': 'close'
    }

    # build the params
    params = {
        'contract': zone,
        'apiKey': API_TOKEN,
        '_': API_ID
    }

    # send the request
    response = requests.get(f'https://{API_HOST}/vls/v3/stations', params=params, headers=headers)

    # check the response status code
    if response.status_code != 200:
        print('Error: Villo: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
