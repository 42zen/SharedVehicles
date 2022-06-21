import requests
import json
import random # TODO: random advertising_id and session_id
import geopy.distance

#API_HOST = 'web-production.lime.bike'

DEVICE_OS_NAME = 'Android'
DEVICE_OS_API_VERSION = '28'
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'

APP_NAME = 'Lime'
APP_VERSION = '3.55.0'
APP_PACKAGE_NAME = 'com.limebike'
APP_CLIENT_VERSION = '4.9.1'

class api:

    token = None # Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3Rva2VuIjoiTkZEMlRFWTRWQVFLRiIsImxvZ2luX2NvdW50IjoxfQ.SHJWky5uQBAZpwr6TJj4SLFK2hGBL_pEGVmlRgJdkFQ
    device_token = None # 38394413-226f-4639-a6a8-c9e1da386c0b
    device_id = None # 913c5974-3d28-4fb5-abbd-0d780eb09564R
    advertising_id = None # 34d302b0-6e80-4387-98ee-b0a1086b3295
    session_id = None # 1654451302275
    registration_id = None # et9j9_k3SnSoz-v2JfzT6N:APA91bHtF_xbpbdMEJlP-xbGkllBVDXJSQTguBqYsJ03Fw5-pJyBtj7obp05s9ggq4_LNUoTj3uOFVcTsJnv0NTGwn_QEbqeKurNQoYhTteuWrXCYzyWXN5A_xPt8zdkeGHZPhkUnaj0

    def set_token(token):
        api.token = token

    def set_device_infos(device_id, device_token):
        api.device_id = device_id
        api.device_token = device_token

    def set_advertising_id(advertising_id):
        api.advertising_id = advertising_id

    def set_session_id(session_id):
        api.session_id = session_id

    def set_registration_id(registration_id):
        api.registration_id = registration_id

    class request:

        def build_headers(api_name):
            headers = {
                'Host': f'{api_name}.lime.bike',
                'App-Version': APP_VERSION,
                'User-Agent': f'{DEVICE_OS_NAME} {APP_NAME}/{APP_VERSION}; ({APP_PACKAGE_NAME}; build:{APP_VERSION}; {DEVICE_OS_NAME} {DEVICE_OS_API_VERSION}) {APP_CLIENT_VERSION}',
                'X-Device-Token': api.device_token,
                'X-Amplitude-Device-Id': api.device_id,
                'Platform': DEVICE_OS_NAME,
                'Connection-Quality': 'POOR',
                'Average-Download-Kbitspersecond': '113.2020',
                'X-Advertising-Id': api.advertising_id,
                'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION}',
                'X-Session-Id': api.session_id,
                'Authorization': api.token,
                'Mobile-Registration-Id': api.registration_id
            }
            return headers

        def request(api_name, endpoint, params=None, req=requests.get):
            headers = api.request.build_headers(api_name)
            if headers == None:
                return None
            url = f'https://{api_name}.lime.bike/{endpoint}'
            response = req(url, headers=headers, params=params)
            return response

        def get(api_name, endpoint, params=None):
            return api.request.request(api_name, endpoint, params=params)

        def post(api_name, endpoint, params=None):
            return api.request.request(api_name, endpoint, params=params, req=requests.post)

    class web_production:
        
        def get(endpoint, params=None):
            response = api.request.get('web-production', endpoint, params=params)
            return json.loads(response.content)
        
        def post(endpoint, params=None):
            response = api.request.post('web-production', endpoint, params=params)
            return json.loads(response.content)

        def get_vehicles(lat, lng, radius=1.0, zoom=16):
            params = {
                'ne_lat': lat + radius,
                'ne_lng': lng + radius,
                'sw_lat': lat - radius,
                'sw_lng': lng - radius,
                'user_latitude': lat,
                'user_longitude': lng,
                'zoom': zoom,
            }
            return api.web_production.get(f'api/rider/v1/views/map', params=params)

        def ring_vehicle(vehicle_id):
            params = { 'id': vehicle_id }
            response = api.web_production.post(f'api/rider/v1/actions/ring_bike', params=params)

    def login(token):
        api.set_token(token)

    def sort_vehicles_by_distance(vehicle):
        return vehicle['distance']

    def get_nearby_vehicles(lat, lng, radius=1000.0, max_vehicles=None, session=None):
        response = api.web_production.get_vehicles(lat, lng)
        vehicles_list = []
        for infos in response['data']['attributes']['bikes']:
            distance = geopy.distance.geodesic((infos['attributes']['latitude'], infos['attributes']['longitude']), (lat, lng)).m
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
        self.lat = infos['attributes']['latitude']
        self.lng = infos['attributes']['longitude']
        self.battery = infos['attributes']['battery_percentage']
        self.name = infos['attributes']['plate_number']
        self.session = session

    def ring(self):
        if self.session != None:
            self.session.context.save_legacy()
            self.session.context.restore_session()
        response = api.web_production.ring_vehicle(self.infos['id'])
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
        self.lat = None
        self.lng = None
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
        result = api.get_nearby_vehicles(lat=lat, lng=lng, radius=radius, max_vehicles=max_vehicles, session=self)
        self.context.save_session()
        self.context.restore_legacy()
        return result
