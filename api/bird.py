#from pickletools import read_unicodestring1
import requests
import json
import random
import datetime
import geopy.distance

APP_NAME = 'bird'
APP_TYPE = 'rider'
APP_VERSION = '4.189.0.9'

DEVICE_MODEL = 'AOSP on IA Emulator'
DEVICE_OS = 'Android'
DEVICE_OS_VERSION = '9'
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'
DEVICE_ARCH = 'generic_x86_arm'

class api:

    class request:
        def build_timestamp():
            timestamp = datetime.datetime.utcnow().isoformat()
            return timestamp[:timestamp.find('.') + 1] + '000+02:00'

        def build_random_device_id():
            charset = "0123456789abcdef"
            device_id = ''
            for i in range(0, 15):
                r = random.randint(0, 15)
                a = charset[r]
                device_id += a
            return device_id

        def build_location(lat, lng, accuracy=20.048999786376953, altitude=0.0, heading=None, mocked=False, source="gps", speed=0.0):
            location = {
                    "accuracy": accuracy,
                    "altitude": altitude,
                    "heading": heading,
                    "latitude": lat,
                    "longitude": lng,
                    "mocked": mocked,
                    "source": source,
                    "speed": speed,
                    "timestamp": api.request.build_timestamp()
            }
            return location

        def build_headers(api_name, location, token=None, device_id=None):
            headers = {
                'Host': f'api-{api_name}.prod.birdapp.com',
                'App-Version': APP_VERSION,
                'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION},{DEVICE_LANG}',
                'Battery-Level': '100',
                'Bluetooth-State': 'disabled',
                'Carrier-Name': DEVICE_OS,
                'Client-Time': api.request.build_timestamp(),
                'Connection-Type': 'unknown',
                'Device-Model': DEVICE_MODEL,
                'Device-Name': DEVICE_ARCH,
                'Device-Region': DEVICE_REGION,
                'Device-Language': DEVICE_LANG,
                'Mobile-Network-Generation': 'unknown',
                'Os-Version': DEVICE_OS_VERSION,
                'Platform': DEVICE_OS.lower(),
                'User-Agent': f'{DEVICE_OS} - {DEVICE_OS_VERSION}',
                'App-Name': APP_NAME,
                'App-Type': APP_TYPE,
                'Content-Type': 'application/json; charset=UTF-8'
            }
            if location != None:
                headers['Location'] = json.dumps(location, separators=(',', ':'))
            if device_id == None:
                device_id = api.request.build_random_device_id()
            headers['Device-Id'] = device_id
            headers['Bird-Device-Id'] = device_id
            if token != None:
                headers['Authorization'] = 'Bearer ' + token
            return headers

        def request(api_name, endpoint, lat=None, lng=None, params=None, json_data=None, req=requests.get, token=None, device_id=None):
            location = None
            if lat != None and lng != None:
                location = api.request.build_location(lat, lng)
            headers = api.request.build_headers(api_name, location, token=token, device_id=device_id)
            url = f'https://api-{api_name}.prod.birdapp.com/{endpoint}'
            if req != requests.get:
                return req(url, headers=headers, params=params, json=json_data)
            return req(url, headers=headers, params=params)

        def get(api_name, endpoint, params=None, token=None, device_id=None, lat=None, lng=None):
            return api.request.request(api_name, endpoint, params=params, token=token, device_id=device_id, lat=lat, lng=lng)

        def post(api_name, endpoint, params=None, json_data=None, token=None, device_id=None, lat=None, lng=None):
            return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=requests.post, token=token, device_id=device_id, lat=lat, lng=lng)

        def put(api_name, endpoint, params=None, json_data=None, token=None, device_id=None, lat=None, lng=None):
            return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=requests.put, token=token, device_id=device_id, lat=lat, lng=lng)

    # this class is useless
    '''
    class analytics:
        def post(endpoint, json_data):
            return api.request.post('analytics', f'analytics/{endpoint}', json_data=json_data)

        def track(events):
            json_data = { 'events': events }
            response = api.analytics.post('analytics', 'track', json_data=json_data)
            return json.loads(response.content)

        def track_events(events=[]):
            json_data = { 'events': events }
            response = api.analytics.post('analytics', 'track-events', json_data=json_data)
            return json.loads(response.content)
    '''

    class auth:
        def post(endpoint, json_data=None, refresh_token=None, device_id=None):
            response = api.request.post('auth', f'api/v1/auth/{endpoint}', json_data=json_data, token=refresh_token, device_id=device_id)
            return json.loads(response.content)

        def get_tokens_from_email(email, device_id=None):
            json_data = { 'email': email }
            response = api.auth.post('email', json_data=json_data, device_id=device_id)
            return response

        def get_tokens_from_email_verification(code, device_id=None):
            json_data = { 'token': code }
            response = api.auth.post('magic-link/use', json_data=json_data, device_id=device_id)
            return response

        def get_tokens_from_refresh_token(refresh_token, device_id=None):
            return api.auth.post('refresh/token', refresh_token=refresh_token, device_id=device_id)

    class bird:
        def get(endpoint, params=None, access_token=None, device_id=None, lat=None, lng=None):
            response = api.request.get('bird', endpoint, params=params, token=access_token, device_id=device_id, lat=lat, lng=lng)
            return json.loads(response.content)

        def put(endpoint, json_data=None, params=None, access_token=None, device_id=None, lat=None, lng=None):
            response = api.request.put('bird', endpoint, json_data=json_data, token=access_token, device_id=device_id, lat=lat, lng=lng)
            return json.loads(response.content)

        def post(endpoint, json_data=None, access_token=None, device_id=None, lat=None, lng=None):
            response = api.request.post('bird', endpoint, json_data=json_data, token=access_token, device_id=device_id, lat=lat, lng=lng)
            return json.loads(response.content)

        def get_alerts(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('alerts', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_announcements(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('announcements', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_area_nearby(lat, lng, radius=5000.0, include_merged=True, access_token=None, device_id=None):
            params = {
                'latitude': lat,
                'longitude': lng,
                'radius': radius,
                'include_merged': include_merged
            }
            return api.bird.get('area/nearby', params=params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def set_bird_chirp(bird_id, alarm=False, access_token=None, device_id=None, lat=None, lng=None):
            json_data = {
                'alarm': alarm,
                'bird_id': bird_id
            }
            return api.bird.put('bird/chirp', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def set_bird_missing(bird_id, request_role='rider', access_token=None, device_id=None, lat=None, lng=None):
            json_data = {
                'bird_id': bird_id,
                'request_role': request_role
            }
            return api.bird.put('bird/missing', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_bird_nearby(lat, lng, radius=5000.0, access_token=None, device_id=None):
            params = {
                'latitude': lat,
                'longitude': lng,
                'radius': radius
            }
            return api.bird.get('bird/nearby', params=params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def is_communication_opted_in(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('communication-opt-in/is-opted-in', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_complaint_schema(type='community', access_token=None, device_id=None, lat=None, lng=None):
            params = { 'type': type }
            return api.bird.get('complaint/schema', params=params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_config(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('config', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_contractor_available_apps(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('contractor/available-applications', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def set_next_contractor_onboard_steps(contractor_level=None, country='US', fields={}, root_field_id=None, access_token=None, device_id=None, lat=None, lng=None):
            json_data = {
                'contractor_level': contractor_level,
                'country': country,
                'fields': fields,
                'root_field_id': root_field_id,
            }
            return api.bird.post('contractor/onboard-steps/next', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_coupon(redeemed=False, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'redeemed': redeemed }
            return api.bird.get('coupon', params=params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_coupon_promo(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('coupon/promotions', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_link(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('link', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_nearby_parking_nests(radius=5000.0, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'radius': radius }
            return api.bird.get('nest/nearby-parking-nests', params=params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_partner_by_id(id, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'id': id }
            return api.bird.get('partner/by-id', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_all_private_bird(offset=0, limit=100, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'offset': offset, 'limit': limit }
            return api.bird.get('private-bird/all', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_ride_pass(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('ride-pass/ui/v2', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_stripe_key(api_version='2020-03-02', access_token=None, device_id=None, lat=None, lng=None): # others: api_version='2017-06-05'
            json_data = { 'api_version': api_version }
            return api.bird.post('stripe/key', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_user(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('user', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_user_balance(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('user/balance', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def push_user(platform='android', sandbox=False, token=None, access_token=None, device_id=None, lat=None, lng=None):
            json_data = {
                'platform': platform,
                'sandbox': sandbox,
                'token': token,
            }
            return api.bird.put('user/push', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def update_user(agreed_at=None, birthdate=None, email=None, image_url=None, locale='en-US', name=None, phone=None, warehouse_id=None, access_token=None, device_id=None, lat=None, lng=None):
            json_data = {
                'agreed_at': agreed_at,
                'birthdate': birthdate,
                'email': email,
                'image_url': image_url,
                'locale': locale,
                'name': name,
                'phone': phone,
                'warehouse_id': warehouse_id,
            }
            return api.bird.put('user/update', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_user_transacion_history(offset=0, limit=50, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'offset': offset, 'limit': limit }
            return api.bird.get('user/transaction-history', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_user_agreement(role='RIDER', partner_id=None, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'role': role }
            if partner_id != None:
                params['partner_id'] = partner_id
            return api.bird.get('user-agreement', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_merchant_by_user_id(id, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'id': id }
            return api.bird.get('v1/merchant/byUserId', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_coupon_by_coupon_id(coupon_ids=[], access_token=None, device_id=None, lat=None, lng=None):
            json_data = { 'coupon_ids': coupon_ids }
            return api.bird.post('v1/merchant/coupon-extension/by-coupon-ids', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_payment_reload_config(currency='eur', access_token=None, device_id=None, lat=None, lng=None):
            params = { 'currency': currency }
            return api.bird.get('v1/payment/charge/reload-config', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_payment_default_provider(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('v1/payment/provider/default', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_payment_provider_token(user_id, kind='braintree', access_token=None, device_id=None, lat=None, lng=None):
            json_data = { 'kind': kind, 'user_id': user_id }
            return api.bird.post('v1/payment/provider/token', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_active_tutorial(access_token=None, device_id=None, lat=None, lng=None):
            return api.bird.get('v1/tutorial/active', access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def get_payment_method_list(user_id, access_token=None, device_id=None, lat=None, lng=None):
            params = { 'user_id': user_id }
            return api.bird.get('v3/payment-method/list', params, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

        def zendesk_login(return_to="https://help.bird.co", access_token=None, device_id=None, lat=None, lng=None):
            json_data = { 'return_to': return_to }
            return api.bird.post('zendesk/login', json_data=json_data, access_token=access_token, device_id=device_id, lat=lat, lng=lng)

    class birdplus:
        def get(endpoint, access_token=None, device_id=None):
            response = api.request.get('birdplus', f'api/v1/{endpoint}', token=access_token, device_id=device_id)
            return json.loads(response.content)

        def birdplus(access_token=None, device_id=None):
            return api.birdplus.get('bird-plus', access_token=access_token, device_id=device_id)

    class itemlease:
        def get(endpoint, access_token=None, device_id=None):
            response = api.request.get('itemlease', f'api/v1/itemlease/{endpoint}', token=access_token, device_id=device_id)
            return json.loads(response.content)

        def active_leases(access_token=None, device_id=None):
            return api.itemlease.get('active-leases', access_token=access_token, device_id=device_id)

    class localization:
        def get(endpoint, params, access_token=None, device_id=None):
            response = api.request.get('localization', f'api/v1/localization/{endpoint}', params=params, token=access_token, device_id=device_id)
            return json.loads(response.content)

        def ota_pull(project_id, modified_after=None, access_token=None, device_id=None):
            if modified_after == None:
                modified_after = api.request.build_timestamp()
            params = { 'bird_project_id': project_id, 'modified_after': modified_after }
            return api.localization.get('ota/pull', params, access_token=access_token, device_id=device_id)

    class rider:
        def get(endpoint, params=None, access_token=None, device_id=None):
            response = api.request.get('rider', f'/{endpoint}', params=params, token=access_token, device_id=device_id)
            return json.loads(response.content)

        def put(endpoint, params, access_token=None, device_id=None):
            response = api.request.put('rider', f'/{endpoint}', params=params, token=access_token, device_id=device_id)
            return json.loads(response.content)

        def get_all_long_term_rental(offset=0, limit=1, active=True, access_token=None, device_id=None):
            params = { 'offset': offset, 'limit': limit, 'active': active }
            return api.rider.get('long-term-rental/all', params, access_token=access_token, device_id=device_id)

        def get_active_multi_ride(access_token=None, device_id=None):
            return api.rider.get('multi-ride/active', access_token=access_token, device_id=device_id)

        def get_active_reservation(access_token=None, device_id=None):
            return api.rider.get('reservation/active', access_token=access_token, device_id=device_id)

        def last_ride_lock_compliance(access_token=None, device_id=None):
            return api.rider.get('ride/last-lock-compliance', access_token=access_token, device_id=device_id)

        def set_acceleration_level(acceleration_level, access_token=None, device_id=None):
            if acceleration_level != 'advanced' and acceleration_level != 'intermediate':
                print(f'Error: Unknown acceleration level {acceleration_level}.')
                return None
            json_data = { 'acceleration_level': acceleration_level }
            return api.rider.put('rider-profile', json_data, access_token=access_token, device_id=device_id)

        def get_beginner_mode_options(access_token=None, device_id=None):
            return api.rider.get('rider-profile/ui/beginner-mode-options', access_token=access_token, device_id=device_id)

# TODO: class Vehicle:
# TODO:     def unlock(self):
# TODO:     def lock(self):
# TODO:     def ring(self):
# TODO:     def alarm(self):
# TODO:     def get_battery(self):
# TODO:     def get_pos(self):
# TODO:     def set_missing(self):
# TODO:     def get_infos(self):
# TODO:     def get_price(self):
# TODO:     def is_free(self):

class Session:
    def set_tokens_filename(self, tokens_filename):
        self.tokens_filename = tokens_filename

    def save_tokens_file(self):
        if self.tokens_filename == None or self.tokens == None:
            return False
        tokens_file = open(self.tokens_filename, 'w')
        json.dump(self.tokens, tokens_file)
        tokens_file.close()
        return True

    def load_tokens_file(self):
        if self.tokens_filename == None:
            return False
        tokens_file = None
        try:
            tokens_file = open(self.tokens_filename, 'r')
        except FileNotFoundError:
            pass
        if tokens_file != None:
            self.tokens = json.load(tokens_file)
            tokens_file.close()
            return True
        return False

    def __init__(self, lat=None, lng=None, tokens_filename=None, device_id=None):
        self.tokens = None
        self.tokens_filename = None
        if tokens_filename != None:
            self.set_tokens_filename(tokens_filename)
            if self.load_tokens_file() == False:
                print("Bird: Warning: Session.__init__: Couldn't read '%s' tokens file." % tokens_filename)
        if device_id == None:
            device_id = api.request.build_random_device_id()
        self.device_id = device_id
        self.lat = lat
        self.lng = lng

    def set_position(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def set_tokens(self, tokens):
        self.tokens = tokens
        self.save_tokens_file()

    def register(self, email):
        response = api.auth.get_tokens_from_email(email, device_id=self.device_id)
        if 'validation_required' not in response:
            print("Bird: Error: Session.register: api.auth.get_tokens_from_email returned", response)
            return False
        if response['validation_required'] == False:
            self.set_tokens(response['tokens'])
            return True
        return False

    def send_email_code(self, email):
        response = api.auth.get_tokens_from_email(email, device_id=self.device_id)
        if 'validation_required' not in response:
            print("Bird: Error: Session.login_from_email: api.auth.get_tokens_from_email returned", response)
            return False
        if response['validation_required'] == False:
            self.set_tokens(response['tokens'])
            print("Bird: Warning: Session.login_from_email: You just created an account for", email)
            return False
        return True

    def login_from_email_code(self, code):
        response = api.auth.get_tokens_from_email_verification(code, device_id=self.device_id)
        if 'access' not in response:
            print("Bird: Error: Session.login_from_email_code: api.auth.get_tokens_from_email_verification returned", response)
            return False
        self.set_tokens(response)
        return True

    def refresh_tokens(self):
        if self.tokens == None:
            print("Bird: Warning: Session.refresh_tokens: You can't refresh tokens without initial token.")
            return False
        refresh_token = self.tokens['refresh']
        response = api.auth.get_tokens_from_refresh_token(refresh_token, device_id=self.device_id)
        if 'access' not in response:
            print("Bird: Error: Session.refresh_session: api.auth.get_tokens_from_refresh_token returned", response)
            return False
        self.set_tokens(response)
        return True

    def login(self, email_code=None, tokens_filename=None):
        if tokens_filename != None:
            self.set_tokens_filename(tokens_filename)
        if email_code != None:
            tokens = self.login_from_email_code(email_code)
            self.set_tokens(tokens)
            return True
        if self.load_tokens_file() == False:
            return False
        self.refresh_tokens()
        return True

    def sort_vehicles_by_distance(self, vehicle):
        return vehicle['distance']

    def get_vehicles_nearby(self, lat=None, lng=None, radius=300.0, max_vehicles=None):
        if self.tokens == None:
            print("Bird: Warning: Session.get_vehicles_nearby: You can't get vehicles nearby without access token.")
            return False
        if lat != None and lng != None:
            self.set_position(lat, lng)
        response = api.bird.get_bird_nearby(self.lat, self.lng, access_token=self.tokens['access'], device_id=self.device_id)
        if 'birds' not in response:
            if 'code' not in response:
                print("Bird: Error: Session.vehicles_nearby: api.bird.get_bird_nearby returned", response)
                return None
            if response['code'] == 401:
                self.refresh_tokens()
                return self.get_vehicles_nearby(lat=lat, lng=lng, radius=radius, max_vehicles=max_vehicles)
            print("Bird: Error: Session.vehicles_nearby: unknown error code", response['code'], ':', response)
            return None
        vehicles_list = []
        for infos in response['birds']:
            distance = geopy.distance.geodesic((infos['location']['latitude'], infos['location']['longitude']), (self.lat, self.lng)).m
            if distance > radius:
                continue
            vehicles_list += [ {
                'infos': infos,
                'distance': distance
            } ]
        vehicles_list.sort(key=self.sort_vehicles_by_distance)
        if max_vehicles != None and len(vehicles_list) > max_vehicles:
            vehicles_list = vehicles_list[:max_vehicles]
        return vehicles_list

sess = Session(lat=50.846885386381636, lng=4.357265272965748, tokens_filename='test.tokens')
vehicles_list = sess.get_vehicles_nearby(radius=20.0)
print(len(vehicles_list))

