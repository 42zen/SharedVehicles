import requests
import json
import geopy.distance


"""
Informations used by the API
"""
API_HOST = 'node.bolt.eu'
API_RING_HOST = 'westeu-rental.taxify.eu'
API_TOKEN = 'Basic KzMzNjk1NzkwMjU4OjVjMGI5NzIzLTkxM2EtNDJiNi1hNDJmLTYzNTZmNzY3NzYyZg=='
API_RING_TOKEN = 'Basic KzMzNjk1NzkwMjU4OjFiZWY3ZDhjLWUwNTctNGJmNi1hYzZkLTkyNWQwNTA2YmUzZQ=='
API_USERID = '118141060'
API_DEVICE_ID = 'cTP5F0PBQIC2jKsSavm-px'
API_SESSION_ID = '118141060u1653238406480'

DEVICE_BRAND = 'Google'
DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_OS_NAME = 'android'
DEVICE_OS_VERSION = 9
DEVICE_COUNTRY = 'be'
DEVICE_LANG = 'en'

APP_CLIENT = 'okhttp/4.9.1'
APP_VERSION = 'CA.40.2'
APP_PAYMENT_ID = '5916512602877075'
APP_PAYMENT_TYPE = 'adyen'


class api:

    """
    Send an API request
    """
    def request(endpoint, lat, lng, post=False, host=API_HOST, token=API_TOKEN, device_id=API_DEVICE_ID, session_id=API_SESSION_ID):
        # build the headers
        headers = {
            'Host': host,
            'Authorization': token,
            'User-Agent': APP_CLIENT
        }
        if post == True:
            headers['Content-Type'] = 'application/x-www-form-urlencoded',

        # build the params
        params = {
            'version': APP_VERSION,
            'deviceId': device_id,
            'device_name': f'{DEVICE_BRAND}{DEVICE_NAME}',
            'device_os_version': DEVICE_OS_VERSION,
            'channel': 'googleplay',
            'deviceType': {DEVICE_OS_NAME},
            'country': DEVICE_COUNTRY,
            'language': DEVICE_LANG,
            'gps_lat': lat,
            'gps_lng': lng,
            'user_id': API_USERID,
            'session_id': session_id
        }
        if host == API_HOST:
            params['lat'] = lat
            params['lng'] = lng
            params['select_all'] = 'true'
            params['payment_method_id'] = APP_PAYMENT_ID
            params['payment_method_type'] = APP_PAYMENT_TYPE

        # build the url
        url = f'https://{host}/{endpoint}'

        # send the request
        if post == True:
            response = requests.post(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers, params=params)

        # return the response
        return response

    """
    Send an API GET request
    """
    def get(endpoint, lat, lng, host=API_HOST, token=API_TOKEN, device_id=API_DEVICE_ID, session_id=API_SESSION_ID):
        return api.request(endpoint, lat, lng, post=False, host=host, token=token, device_id=device_id, session_id=session_id)

    """
    Send an API POST request
    """
    def post(endpoint, lat, lng, host=API_HOST, token=API_TOKEN, device_id=API_DEVICE_ID, session_id=API_SESSION_ID):
        return api.request(endpoint, lat, lng, post=True, host=host, token=token, device_id=device_id, session_id=session_id)


    """
    Get the shared vehicles list
    """
    def get_vehicles(lat, lng):
        # send the request
        response = api.get('rental-search/categoriesOverview', lat, lng)

        # check the response status code
        if response.status_code != 200:
            print('Error: Bolt: get_vehicles: Invalid status code: %i.' % response.status_code)
            return None

        # return the parsed response
        return json.loads(response.content)

    """
    Ring a specific vehicle
    """
    def ring_vehicle(id, lat, lng, device_id='dr4Qxu6XRKuHZ1Htr4nBr1', session_id='118141060u1654863795716'):
        # build the data
        data = 'vehicle_id=%s' % id

        # send the request
        response = api.post('client/ringVehicle', lat, lng, data, host=API_RING_HOST, token=API_RING_TOKEN, device_id=device_id, session_id=session_id)

        # check the response status code
        if response.status_code != 200:
            print('Error: Bolt: ring_vehicle: Invalid status code: %i.' % response.status_code)
            if response.content != None:
                print(response.content)
            return None

        # return the parsed response
        return json.loads(response.content)


"""
Check the vehicle model for any API changes

Current Model:
{
    "id":396978,
    "name":"XXX-643",
    "type":"scooter",
    "lat":50.82781982421875,
    "lng":4.411500453948975,
    "charge":67,
    "distance_on_charge":21240,
    "search_category_id":705,
    "primary_action":"reserve"
}
"""
def check_vehicle_model(vehicle):
    # list all known fields
    known_fields = ['id', 'name', 'type', 'lat', 'lng', 'charge', 'distance_on_charge', 'search_category_id', 'primary_action']

    # check for missing fields
    for field in known_fields:
        if field not in vehicle:
            print("Warning: Bolt: Missing %s field." % field)

    # check for new fields
    for field in vehicle:
        if field not in known_fields:
            print("Warning: Bolt: Unknown %s field." % field)

"""
Get the shared vehicles list
"""
def get_vehicles(lat, lng, radius=None):
    # request the vehicles list from the api
    response = api.get_vehicles(lat, lng)
    if response == None:
        return None

    # build the vehicles list
    vehicles_list = []
    for categorie in response['data']['categories']:
        for vehicle_info in categorie['vehicles']:
            check_vehicle_model(vehicle_info)
            vehicle_lat = vehicle_info['lat']
            vehicle_lng = vehicle_info['lng']
            dist = geopy.distance.geodesic((lat, lng), (vehicle_lat, vehicle_lng)).m
            if radius == None or dist <= radius:
                vehicle = {
                    'brand': 'Bolt',
                    'lat': vehicle_lat,
                    'lng': vehicle_lng,
                    'battery': vehicle_info['charge'],
                    'distance': dist,
                    'infos': vehicle_info
                }
                vehicles_list += [vehicle]

    # return the vehicle list
    return vehicles_list

"""
Ring a specific vehicle
"""
def ring_vehicle(vehicle):
    # request the vehicle ring from the api
    response = api.ring_vehicle(vehicle['infos']['id'], vehicle['lat'], vehicle['lng'])

    # check the response
    if response == None:
        return False

    # vehicle is ringing
    return True
