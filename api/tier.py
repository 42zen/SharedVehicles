import requests
import json
import geopy.distance

DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = 9

APP_NAME = 'Tier'
APP_VERSION = '4.0.43'

class api:

    token = None # iPtAHWdOVLEtgkaymXoMHVVg

    def set_token(token):
        api.token = token

    class request:

        def build_headers(api_name):
            headers = {
                'Host': f'{api_name}.tier-services.io',
                'Customer-Agent': f'{APP_NAME} {DEVICE_OS_NAME}',
                'X-Api-Key': api.token,
                'User-Agent': f'{APP_NAME.upper()}/{APP_VERSION} ({DEVICE_OS_NAME}/{DEVICE_OS_VERSION})'
            }
            return headers

        def request(api_name, endpoint, params=None, req=requests.get):
            headers = api.request.build_headers(api_name)
            if headers == None:
                return None
            url = f'https://{api_name}.tier-services.io/{endpoint}'
            response = req(url, headers=headers, params=params)
            return response

        def get(api_name, endpoint, params=None):
            return api.request.request(api_name, endpoint, params=params)

        def post(api_name, endpoint):
            return api.request.request(api_name, endpoint, req=requests.post)

    class platform:
        
        def get(endpoint, params=None):
            response = api.request.get('platform', endpoint, params=params)
            return json.loads(response.content)
        
        def post(endpoint):
            response = api.request.post('platform', endpoint)
            return json.loads(response.content)

        def get_zones():
            return api.platform.get('v1/zone')
        
        def get_vehicles_from_position(lat, lng, radius=300):
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
            return api.platform.get('v2/vehicle', params=params)
        
        def get_vehicles_from_zone_id(zone_id):
            params = {
                'type[]': [
                    'escooter',
                    'ebicycle',
                    'emoped'
                ],
                'zoneId': zone_id
            }
            return api.platform.get('v2/vehicle', params=params)
        
        '''
        # is this an exploit ?
        def get_all_vehicles():
            params = {
                'type[]': [
                    'escooter',
                    'ebicycle',
                    'emoped'
                ],
                'radius': 1 # maybe 10000000
            }
            return api.platform.get('vehicle', params=params)
        '''

        def flash_vehicle(vehicle_id):
            return api.platform.post(f'v1/vehicle/{vehicle_id}/flash')

    def login(token):
        api.set_token(token)

    def sort_vehicles_by_distance(vehicle):
        return vehicle['distance']

    def get_nearby_vehicles(lat, lng, radius=1000.0, max_vehicles=None, session=None):
        response = api.platform.get_vehicles_from_position(lat, lng)
        vehicles_list = []
        for infos in response['data']:
            distance = geopy.distance.geodesic((infos['attributes']['lat'], infos['attributes']['lng']), (lat, lng)).m
            if distance > radius:
                continue
            vehicles_list += [ {
                'infos': infos,
                'distance': distance
            } ]
        vehicles_list.sort(key=api.sort_vehicles_by_distance)
        if max_vehicles != None and len(vehicles_list) > max_vehicles:
            vehicles_list = vehicles_list[:max_vehicles]
        vehicles_final_list = []
        for vehicle in vehicles_list:
            vehicles_final_list += [Vehicle(vehicle['infos'], session=session, distance=vehicle['distance'])]
        return vehicles_final_list

class Vehicle:
    def __init__(self, infos, session=None, distance=None):
        self.infos = infos
        self.distance = distance
        self.lat = infos['attributes']['lat']
        self.lng = infos['attributes']['lng']
        self.battery = infos['attributes']['batteryLevel']
        self.name = infos['attributes']['code']
        self.session = session

    def ring(self):
        if self.session != None:
            self.session.context.save_legacy()
            self.session.context.restore_session()
        response = api.platform.flash_vehicle(self.infos['id'])
        if self.session != None:
            self.session.context.save_session()
            self.session.context.restore_legacy()
        return response

    # TODO: def alarm(self):
    # TODO: def set_missing(self):

    # TODO: def get_price(self):
    # TODO: def is_free(self):

    # TODO: def unlock(self):
    # TODO: def lock(self):

class context:
    def __init__(self):
        self.token = None

    def save_legacy(self):
        self.leg_token = api.token

    def restore_legacy(self):
        api.token = self.leg_token

    def save_session(self):
        self.token = api.token

    def restore_session(self):
        api.token = self.token

class Session:
    def __init__(self):
        self.context = context()

    def login(self, token):
        self.context.save_legacy()
        self.context.restore_session()
        api.login(token)
        self.context.save_session()
        self.context.restore_legacy()
        return True

    def get_nearby_vehicles(self, lat, lng, radius=300.0, max_vehicles=None):
        self.context.save_legacy()
        self.context.restore_session()
        result = api.get_nearby_vehicles(lat, lng, radius=radius, max_vehicles=max_vehicles, session=self)
        self.context.save_session()
        self.context.restore_legacy()
        return result