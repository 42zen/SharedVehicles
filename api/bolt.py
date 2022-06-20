import requests
import json
import random
import datetime
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
    token = None      # {'node.bolt.eu':'Basic KzMzNjk1NzkwMjU4OjVjMGI5NzIzLTkxM2EtNDJiNi1hNDJmLTYzNTZmNzY3NzYyZg==', 'westeu-rental.taxify.eu':'Basic KzMzNjk1NzkwMjU4OjFiZWY3ZDhjLWUwNTctNGJmNi1hYzZkLTkyNWQwNTA2YmUzZQ=='}
    user_id = None    # 118141060
    device_id = None  # cTP5F0PBQIC2jKsSavm-px
    session_id = None # 118141060u1653238406480
    payment_id = None # 5916512602877075

    def set_position(lat, lng):
        api.lat = lat
        api.lng = lng

    def set_token(token):
        api.token = token

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
                'Authorization': api.token[api_name],
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
            return api.request.get('node.bolt.eu', endpoint, params=params)

        def get_nearby_vehicles(lat, lng):
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
            return api.request.post('westeu-rental.taxify.eu', endpoint, data=data)

        def ring_vehicle(vehicle_id):
            data = f'vehicle_id={vehicle_id}'
            return api.taxify.post('client/ringVehicle', data=data)

    # TODO: def register()
    # TODO: def login()
    # TODO: def get_nearby_vehicles()

# TODO: class Vehicle
# TODO: class Session
    # TODO: def register()
    # TODO: def login()
    # TODO: def get_nearby_vehicles()

