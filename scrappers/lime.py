import requests
import json
import geopy.distance


"""
Informations used by the API
"""
API_HOST = 'web-production.lime.bike'
API_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3Rva2VuIjoiTkZEMlRFWTRWQVFLRiIsImxvZ2luX2NvdW50IjoxfQ.SHJWky5uQBAZpwr6TJj4SLFK2hGBL_pEGVmlRgJdkFQ'
API_DEVICE_TOKEN = '38394413-226f-4639-a6a8-c9e1da386c0b'
API_DEVICE_ID = '913c5974-3d28-4fb5-abbd-0d780eb09564R'
API_ADVERTISING_ID = '34d302b0-6e80-4387-98ee-b0a1086b3295'
API_SESSION_ID = '1654451302275'
API_REGISTRATION_ID = 'et9j9_k3SnSoz-v2JfzT6N:APA91bHtF_xbpbdMEJlP-xbGkllBVDXJSQTguBqYsJ03Fw5-pJyBtj7obp05s9ggq4_LNUoTj3uOFVcTsJnv0NTGwn_QEbqeKurNQoYhTteuWrXCYzyWXN5A_xPt8zdkeGHZPhkUnaj0'

DEVICE_OS_NAME = 'Android'
DEVICE_OS_API_VERSION = '28'
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_NAME = 'Lime'
APP_VERSION = '3.55.0'
APP_PACKAGE_NAME = 'com.limebike'
APP_CLIENT_VERSION = '4.9.1'


class api:

    """
    Send an API request
    """
    def request(endpoint, params=None, post=False):
        # build the headers
        headers = {
            'Host': API_HOST,
            'App-Version': APP_VERSION,
            'User-Agent': f'{DEVICE_OS_NAME} {APP_NAME}/{APP_VERSION}; ({APP_PACKAGE_NAME}; build:{APP_VERSION}; {DEVICE_OS_NAME} {DEVICE_OS_API_VERSION}) {APP_CLIENT_VERSION}',
            'X-Device-Token': API_DEVICE_TOKEN,
            'X-Amplitude-Device-Id': API_DEVICE_ID,
            'Platform': DEVICE_OS_NAME,
            'Connection-Quality': 'POOR',
            'Average-Download-Kbitspersecond': '113.2020',
            'X-Advertising-Id': API_ADVERTISING_ID,
            'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION}',
            'X-Session-Id': API_SESSION_ID,
            'Authorization': API_TOKEN,
            'Mobile-Registration-Id': API_REGISTRATION_ID
        }

        # build the url
        url = f'https://{API_HOST}/{endpoint}'

        # send the request
        if post == False:
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.post(url, headers=headers, params=params)

        # return the response
        return response

    """
    Send an API GET request
    """
    def get(endpoint, params=None):
        return api.request(endpoint, params=params)

    """
    Send an API POST request
    """
    def post(endpoint, params=None):
        return api.request(endpoint, params=params, post=True)

    """
    Get the shared vehicles list
    """
    def get_vehicles(lat, lng, zoom=16):
        # build the params
        params = {
            'ne_lat': lat + 1.0,
            'ne_lng': lng + 1.0,
            'sw_lat': lat - 1.0,
            'sw_lng': lng - 1.0,
            'user_latitude': lat,
            'user_longitude': lng,
            'zoom': zoom,
        }

        # send the request
        response = api.get(f'api/rider/v1/views/map', params=params)

        # check the response status code
        if response.status_code != 200:
            print('Error: Lime: get_vehicles: Invalid status code: %i.' % response.status_code)
            return None

        # return the parsed response
        return json.loads(response.content)

    """
    Ring a specific vehicle
    """
    def ring_vehicle(vehicle_id):
        # build the params
        params = {
            'id': vehicle_id
        }

        # send the request
        response = api.post(f'api/rider/v1/actions/ring_bike', params=params)

        # check for errors
        if response.status_code == 400:
            err_list = json.loads(response.content)['errors']
            if len(err_list) == 1:
                print('Error: Lime: ring_bike: %s' % err_list[0]['detail'])
            else:
                print('Errors: Lime: ring_bike:')
                for err in err_list:
                    print('%s: %s' % (err['status'], err['detail']))
            return None

        # check the response status code
        if response.status_code != 200:
            print('Error: Lime: ring_bike: Invalid status code: %i.' % response.status_code)
            return None

        # return the parsed response
        return json.loads(response.content)


"""
Check the vehicle model for any API changes

Current Model:
{
    "id": "ET-3HCWFDVMK22UTPMDXRFIMTP4HP4PZKB3IXHQWBA",
    "type": "bikes",
    "attributes": {
        "battery_level": "high",
        "battery_percentage": 64,
        "bike_icon_id": 50,
        "brand": "lime",
        "generation": "3.4",
        "last_activity_at": "2022-06-12T12:11:53.000Z",
        "last_three": "EDG",
        "latitude": 50.853538,
        "license_plate_number": null,
        "longitude": 4.334653,
        "meter_range": 16193,
        "operating_status": "in_service",
        "physical_hardware_with_types": [],
        "plate_number": "XXX-EDG",
        "provider": "Lime",
        "rate_plan": "\u20ac1 to unlock +\n\u20ac0.22 / 1 min",
        "status": "locked",
        "swappable_battery": false,
        "type_name": "scooter"
    }
}
"""
def check_vehicle_model(vehicle):
    # list all known fields
    known_fields = ['id', 'type', 'attributes']

    # check for missing fields
    for field in known_fields:
        if field not in vehicle:
            print("Warning: Lime: Missing %s field." % field)

    # check for new fields
    for field in vehicle:
        if field not in known_fields:
            print("Warning: Lime: Unknown %s field." % field)

    # list all known attributes fields
    known_fields = ['battery_level', 'battery_percentage', 'bike_icon_id', 'brand',
        'generation', 'last_activity_at', 'last_three', 'latitude',
        'license_plate_number', 'longitude', 'meter_range', 'operating_status',
        'physical_hardware_with_types', 'plate_number', 'provider', 'rate_plan',
        'status', 'swappable_battery', 'type_name']

    # check for missing attributes fields
    for field in known_fields:
        if field not in vehicle['attributes']:
            print("Warning: Lime: Missing %s attributes field." % field)

    # check for new attributes fields
    for field in vehicle['attributes']:
        if field not in known_fields:
            print("Warning: Lime: Unknown %s attributes field." % field)

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
    for vehicle_info in response['data']['attributes']['bikes']:
        check_vehicle_model(vehicle_info)
        vehicle_lat = vehicle_info['attributes']['latitude']
        vehicle_lng = vehicle_info['attributes']['longitude']
        dist = geopy.distance.geodesic((lat, lng), (vehicle_lat, vehicle_lng)).m
        if radius == None or dist <= radius:
            vehicle = {
                'brand': 'Lime',
                'lat': vehicle_lat,
                'lng': vehicle_lng,
                'battery': vehicle_info['attributes']['battery_percentage'],
                'distance': dist,
                'infos': vehicle_info
            }
            vehicles_list += [vehicle]

    # return the vehicle list
    return vehicles_list

"""
Ring a specific vehicle
"""
def ring_vehicle(vehicle, position_is_set=False):
    # set the current position to where the vehicle is if needed
    if position_is_set == False:
        api.get_vehicles(vehicle['lat'], vehicle['lng'])

    # request the vehicle ring from the api
    response = api.ring_vehicle(vehicle['infos']['id'])

    # check the response
    if response == None:
        return False

    # vehicle is ringing
    return True
