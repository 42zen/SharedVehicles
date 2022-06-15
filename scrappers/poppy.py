import requests
import json


"""
Informations used by the API
"""
API_HOST = 'poppy.red'

APP_CLIENT = 'okhttp/4.9.1'


"""
Send a request to the API
"""
def _request(endpoint):
    # build the headers
    headers = {
        'Host': API_HOST,
        'Rid': 'anti-csrf',
        'User-Agent': APP_CLIENT
    }

    # send the request
    response = requests.get(f'https://{API_HOST}/api/v2/{endpoint}', headers=headers)

    # return the response
    return response

"""
Get the shared vehicles list
"""
def get_vehicles():
    # request the vehicles list
    response = _request('vehicles')

    # check the response status code
    if response.status_code != 200:
        print('Error: Poppy: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # return the parsed response
    return json.loads(response.content)
