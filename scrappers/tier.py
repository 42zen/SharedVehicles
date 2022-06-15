import requests
import json
import geopy.distance


"""
Informations used by the API
"""
API_HOST = 'platform.tier-services.io'
API_TOKEN = 'iPtAHWdOVLEtgkaymXoMHVVg'

DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = 9

APP_NAME = 'Tier'
APP_VERSION = '4.0.43'


class api:

    """
    Send a request to the API
    """
    def request(endpoint, post=False, params=None):
        # build the headers
        headers = {
            'Host': API_HOST,
            'Customer-Agent': f'{APP_NAME} {DEVICE_OS_NAME}',
            'X-Api-Key': API_TOKEN,
            'User-Agent': f'{APP_NAME.upper()}/{APP_VERSION} ({DEVICE_OS_NAME}/{DEVICE_OS_VERSION})'
        }

        # build the url
        url = f'https://{API_HOST}/{endpoint}'

        # send the request
        if post == True:
            response = requests.post(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers, params=params)

        # check the response status code
        if response.status_code != 200:
            print(f'Error: Tier: {endpoint}: Invalid status code: %i.' % response.status_code)
            if response.content != None:
                print(response.content)
            return None

        # return the parsed response
        return json.loads(response.content)

    """
    Send a GET request to the API
    """
    def get(endpoint, params=None):
        return api.request(endpoint, params=params)

    """
    Send a POST request to the API
    """
    def post(endpoint, params=None):
        return api.request(endpoint, post=True, params=params)

    """
    Get the zones list
    """
    def get_zones():
        # send the request
        return api.get('v1/zone')

    """
    Get the shared vehicles list from zone id
    """
    def get_vehicles(lat, lng, radius=300):
        # build the params
        params = {
            'type[]': [
                'escooter',
                'ebicycle',
                'emoped'
            ],
            'lat': lat,
            'lng': lng,
            'radius': radius
        }

        # send the request
        return api.get('v2/vehicle', params=params)

    """
    Get the shared vehicles list from zone id
    """
    def get_vehicles_from_zone_id(zone_id):
        # build the params
        params = {
            'type[]': [
                'escooter',
                'ebicycle',
                'emoped'
            ],
            'zoneId': zone_id
        }

        # send the request
        return api.get('v2/vehicle', params=params)

    """
    Get all the shared vehicles list
    """
    def get_vehicles_all():
        # build the params
        params = {
            'type[]': [
                'escooter',
                'ebicycle',
                'emoped'
            ],
            'radius': 10000000
        }

        # send the request
        return api.get('vehicle', params=params)

    """
    Ring a vehicle
    """
    def ring_vehicle(vehicle_id):
        return api.post('v1/vehicle/{vehicle_id}/flash')

"""
Check the vehicle model for any API changes

Current Model:
{
    "id": "21044532-17a9-401c-8dca-38383cc02e0d",
    "type": "vehicle",
    "attributes": {
        "batteryLevel": 94,
        "code": 330002,
        "currentRangeMeters": 43000,
        "hasHelmet": false,
        "hasHelmetBox": false,
        "iotVendor": "okai",
        "isRentable": true,
        "lastLocationUpdate": "2022-06-12T15:28:35Z",
        "lastStateChange": "2022-06-10T05:28:36Z",
        "lat": 50.874166,
        "licencePlate": "330002",
        "lng": 4.413613,
        "maxSpeed": 25,
        "state": "ACTIVE",
        "vehicleType": "escooter",
        "zoneId": "BRUSSEL"
    }
}

Current All Model:
{
    "batteryLevel": 96,
    "code": 101619,
    "id": "1d934be4-fed7-474e-af84-aad18c2c1f03",
    "iotVendor": "okai",
    "isRentable": true,
    "lastLocationUpdate": "2022-06-12T15:30:52Z",
    "lastStateChange": "2022-06-09T15:19:30Z",
    "lat": 47.588742,
    "licencePlate": "101619",
    "lng": 19.15338,
    "maxSpeed": 20,
    "state": "ACTIVE",
    "vin": "AA000978",
    "zoneId": "TEST"
}
"""
def check_vehicle_model(vehicle, format_all):
    # TODO: check_vehicle_model
    pass

"""
Get the shared vehicles list
"""
def get_vehicles(lat=None, lng=None, radius=None, zone_id=None):
    # request the vehicles list
    format_all = False
    if lat != None and lng != None:
        response = api.get_vehicles(lat, lng)
    elif zone_id != None:
        response = api.get_vehicles_from_zone_id(zone_id)
    else:
        response = api.get_vehicles_all()
        format_all = True

    # build the vehicles list
    vehicles_list = []
    for vehicle_info in response['data']:
        check_vehicle_model(vehicle_info, format_all)
        if format_all == False:
            vehicle_lat = vehicle_info['attributes']['lat']
            vehicle_lng = vehicle_info['attributes']['lng']
            vehicle_battery = vehicle_info['attributes']['batteryLevel']
        else:
            vehicle_lat = vehicle_info['lat']
            vehicle_lng = vehicle_info['lng']
            vehicle_battery = vehicle_info['batteryLevel']
        dist = geopy.distance.geodesic((lat, lng), (vehicle_lat, vehicle_lng)).m
        if radius == None or dist <= radius:
            vehicle = {
                'brand': 'Tier',
                'lat': vehicle_lat,
                'lng': vehicle_lng,
                'battery': vehicle_battery,
                'distance': dist,
                'infos': vehicle_info
            }
            vehicles_list += [vehicle]

    # return the vehicle list
    return vehicles_list

"""
Ring a vehicle
"""
def ring_vehicle(vehicle, position_is_set=False):
    # set your own position if needed
    if position_is_set == False:
        api.get_vehicles(vehicle['lat'], vehicle['lng'])

    # send the request
    return api.ring_vehicle(vehicle['infos']['id'])
