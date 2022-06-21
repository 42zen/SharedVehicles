import requests
import json
import random # TODO: build random (user, device, session, payment) ids
import geopy.distance

DEVICE_BRAND = 'Google'
DEVICE_NAME = 'AOSP on IA Emulator'
DEVICE_OS_NAME = 'android'
DEVICE_OS_VERSION = 9
DEVICE_COUNTRY = 'be'
DEVICE_LANG = 'en'

APP_CLIENT = 'okhttp/4.9.1'
APP_VERSION = 'CA.40.2'

class api:

    lat = None
    lng = None
    tokens = None      # {'node.bolt.eu':'Basic KzMzNjk1NzkwMjU4OjVjMGI5NzIzLTkxM2EtNDJiNi1hNDJmLTYzNTZmNzY3NzYyZg==', 'westeu-rental.taxify.eu':'Basic KzMzNjk1NzkwMjU4OjFiZWY3ZDhjLWUwNTctNGJmNi1hYzZkLTkyNWQwNTA2YmUzZQ=='}
    user_id = None    # 118141060
    device_id = None  # cTP5F0PBQIC2jKsSavm-px
    session_id = None # 118141060u1653238406480
    payment_id = None # 5916512602877075

    def set_position(lat, lng):
        api.lat = lat
        api.lng = lng

    def set_tokens(tokens):
        api.tokens = tokens

    def set_user_id(user_id):
        api.user_id = user_id

    def set_device_id(device_id):
        api.device_id = device_id

    def set_session_id(session_id):
        api.session_id = session_id

    def set_payment_id(payment_id):
        api.payment_id = payment_id

    class request:

        def build_headers(api_name):
            headers = {
                'Host': api_name,
                'Authorization': api.tokens[api_name],
                'User-Agent': APP_CLIENT
            }
            if api_name == 'westeu-rental.taxify.eu':
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            return headers

        def build_params(added_params):
            params = {
                'version': APP_VERSION,
                'deviceId': api.device_id,
                'device_name': f'{DEVICE_BRAND}{DEVICE_NAME}',
                'device_os_version': DEVICE_OS_VERSION,
                'channel': 'googleplay',
                'deviceType': {DEVICE_OS_NAME},
                'country': DEVICE_COUNTRY,
                'language': DEVICE_LANG,
                'gps_lat': api.lat,
                'gps_lng': api.lng,
                'user_id': api.user_id,
                'session_id': api.session_id
            }
            for param in added_params:
                params[param] = added_params[param]
            return params

        def request(api_name, endpoint, params=None, data=None, req=requests.get):
            headers = api.request.build_headers(api_name)
            params = api.request.build_params(params)
            if headers == None:
                return None
            url = f'https://{api_name}/{endpoint}'
            if req != requests.get:
                response = req(url, headers=headers, params=params, data=data)
            else:
                response = req(url, headers=headers, params=params)
            return response

        def get(api_name, endpoint, params=None):
            return api.request.request(api_name, endpoint, params=params)

        def post(api_name, endpoint, params=None, data=None):
            return api.request.request(api_name, endpoint, params=params, data=data, req=requests.post)

    class node:

        def get(endpoint, params=None):
            response = api.request.get('node.bolt.eu', endpoint, params=params)
            return json.loads(response.content)

        def get_rental_categories(lat, lng):
            api.set_position(lat, lng)
            params = {
                'lat': api.lat,
                'lng': api.lng,
                'select_all': 'true',
                'payment_method_id': api.payment_id,
                'payment_method_type': 'adyen'
            }
            return api.node.get('rental-search/categoriesOverview', params=params)

    class taxify:

        def post(endpoint, data=None):
            response = api.request.post('westeu-rental.taxify.eu', endpoint, data=data)
            return json.loads(response.content)

        def ring_vehicle(vehicle_id):
            data = f'vehicle_id={vehicle_id}'
            return api.taxify.post('client/ringVehicle', data=data)

    # TODO: def register()

    def login(tokens):
        api.set_tokens(tokens)

    def sort_vehicles_by_distance(vehicle):
        return vehicle['distance']

    def get_nearby_vehicles(lat, lng, radius=1000.0, max_vehicles=None, session=None):
        api.set_position(lat, lng)
        response = api.node.get_rental_categories(api.lat, api.lng)
        vehicles_list = []
        for categorie in response['data']['categories']:
            for infos in categorie['vehicles']:
                distance = geopy.distance.geodesic((infos['lat'], infos['lng']), (api.lat, api.lng)).m
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
        self.lat = infos['lat']
        self.lng = infos['lng']
        self.battery = infos['charge']
        self.name = infos['name']
        self.session = session

    def ring(self):
        if self.session != None:
            self.session.context.save_legacy()
            self.session.context.restore_session()
        response = api.taxify.ring_vehicle(self.infos['id'])
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
        self.tokens = None
        self.user_id = None
        self.device_id = None
        self.session_id = None
        self.payment_id = None

    def save_legacy(self):
        self.leg_lat = api.lat
        self.leg_lng = api.lng
        self.leg_tokens = api.tokens
        self.leg_user_id = api.user_id
        self.leg_device_id = api.device_id
        self.leg_session_id = api.session_id
        self.leg_payment_id = api.payment_id

    def restore_legacy(self):
        api.lat = self.leg_lat
        api.lng = self.leg_lng
        api.tokens = self.leg_tokens
        api.user_id = self.leg_user_id
        api.device_id = self.leg_device_id
        api.session_id = self.leg_session_id
        api.payment_id = self.leg_payment_id

    def save_session(self):
        self.lat = api.lat
        self.lng = api.lng
        self.tokens = api.tokens
        self.user_id = api.user_id
        self.device_id = api.device_id
        self.session_id = api.session_id
        self.payment_id = api.payment_id

    def restore_session(self):
        api.lat = self.lat
        api.lng = self.lng
        api.tokens = self.tokens
        api.user_id = self.user_id
        api.device_id = self.device_id
        api.session_id = self.session_id
        api.payment_id = self.payment_id

class Session:
    def __init__(self):
        self.context = context()

    def login(self, tokens):
        self.context.save_legacy()
        self.context.restore_session()
        api.login(tokens)
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
