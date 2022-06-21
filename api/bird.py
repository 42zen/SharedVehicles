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

    lat = None
    lng = None
    location_header = None
    class location:
        accuracy = 20.048999786376953
        altitude = 0.0
        heading = None
        mocked = False
        source = 'gps'
        speed = 0.0
    device_id = None
    tokens = None
    token = None

    def build_location_header():
        api.location_header = {
            "accuracy": api.location.accuracy,
            "altitude": api.location.altitude,
            "heading": api.location.heading,
            "latitude": api.lat,
            "longitude": api.lng,
            "mocked": api.location.mocked,
            "source": api.location.source,
            "speed": api.location.speed,
            "timestamp": api.request.build_timestamp()
        }

    def set_position(lat, lng):
        api.lat = lat
        api.lng = lng
        api.build_location_header()

    def set_location(accuracy, altitude, heading, mocked, source, speed):
        api.location.accuracy = accuracy
        api.location.altitude = altitude
        api.location.heading = heading
        api.location.mocked = mocked
        api.location.source = source
        api.location.speed = speed
        api.build_location_header()

    def set_tokens(tokens):
        api.tokens = tokens
        api.token = tokens['access']

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

        def build_headers(api_name, location, is_guest=False):
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
            if api.device_id == None:
                api.device_id = api.request.build_random_device_id()
            headers['Device-Id'] = api.device_id
            headers['Bird-Device-Id'] = api.device_id
            if is_guest == False:
                if api.token == None:
                    return None
                headers['Authorization'] = 'Bearer ' + api.token
            return headers

        def request(api_name, endpoint, params=None, json_data=None, req=requests.get, is_guest=False):
            headers = api.request.build_headers(api_name, api.location_header, is_guest=is_guest)
            if headers == None:
                return None
            url = f'https://api-{api_name}.prod.birdapp.com/{endpoint}'
            if req != requests.get:
                response = req(url, headers=headers, params=params, json=json_data)
            else:
                response = req(url, headers=headers, params=params)
            if is_guest == False and response.status_code == 401:
                api.refresh_tokens()
                return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=req)
            return response

        def get(api_name, endpoint, params=None):
            return api.request.request(api_name, endpoint, params=params)

        def post(api_name, endpoint, params=None, json_data=None, is_guest=False):
            return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=requests.post, is_guest=is_guest)

        def put(api_name, endpoint, params=None, json_data=None):
            return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=requests.put)

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
        def post(endpoint, json_data=None, is_guest=False):
            response = api.request.post('auth', f'api/v1/auth/{endpoint}', json_data=json_data, is_guest=is_guest)
            return json.loads(response.content)

        def get_tokens_from_email(email):
            json_data = { 'email': email }
            return api.auth.post('email', json_data=json_data, is_guest=True)

        def get_tokens_from_email_verification(code):
            json_data = { 'token': code }
            return api.auth.post('magic-link/use', json_data=json_data, is_guest=True)

        def get_tokens_from_refresh_token():
            token = api.token
            api.token = api.tokens['refresh']
            response = api.auth.post('refresh/token')
            api.token = token
            return response

    class bird:
        def get(endpoint, params=None):
            response = api.request.get('bird', endpoint, params=params)
            return json.loads(response.content)

        def put(endpoint, json_data=None, params=None):
            response = api.request.put('bird', endpoint, json_data=json_data)
            return json.loads(response.content)

        def post(endpoint, json_data=None):
            response = api.request.post('bird', endpoint, json_data=json_data)
            return json.loads(response.content)

        def get_alerts():
            return api.bird.get('alerts')

        def get_announcements():
            return api.bird.get('announcements')

        def get_area_nearby(lat, lng, radius=5000.0, include_merged=True):
            params = {
                'latitude': lat,
                'longitude': lng,
                'radius': radius,
                'include_merged': include_merged
            }
            return api.bird.get('area/nearby', params=params)

        def set_bird_chirp(bird_id, alarm=False):
            json_data = { 'alarm': alarm, 'bird_id': bird_id }
            return api.bird.put('bird/chirp', json_data=json_data)

        def set_bird_missing(bird_id, request_role='rider'):
            json_data = { 'bird_id': bird_id, 'request_role': request_role }
            return api.bird.put('bird/missing', json_data=json_data)

        def get_bird_nearby(lat, lng, radius=5000.0):
            params = {
                'latitude': lat,
                'longitude': lng,
                'radius': radius
            }
            return api.bird.get('bird/nearby', params=params)

        def is_communication_opted_in():
            return api.bird.get('communication-opt-in/is-opted-in')

        def get_complaint_schema(type='community'):
            params = { 'type': type }
            return api.bird.get('complaint/schema', params=params)

        def get_config():
            return api.bird.get('config')

        def get_contractor_available_apps():
            return api.bird.get('contractor/available-applications')

        def set_next_contractor_onboard_steps(contractor_level=None, country='US', fields={}, root_field_id=None):
            json_data = {
                'contractor_level': contractor_level,
                'country': country,
                'fields': fields,
                'root_field_id': root_field_id,
            }
            return api.bird.post('contractor/onboard-steps/next', json_data=json_data)

        def get_coupon(redeemed=False):
            params = { 'redeemed': redeemed }
            return api.bird.get('coupon', params=params)

        def get_coupon_promo():
            return api.bird.get('coupon/promotions')

        def get_link():
            return api.bird.get('link')

        def get_nearby_parking_nests(radius=5000.0):
            params = { 'radius': radius }
            return api.bird.get('nest/nearby-parking-nests', params=params)

        def get_partner_by_id(id):
            params = { 'id': id }
            return api.bird.get('partner/by-id', params)

        def get_all_private_bird(offset=0, limit=100):
            params = { 'offset': offset, 'limit': limit }
            return api.bird.get('private-bird/all', params)

        def get_ride_pass():
            return api.bird.get('ride-pass/ui/v2')

        def get_stripe_key(api_version='2020-03-02'): # others: api_version='2017-06-05'
            json_data = { 'api_version': api_version }
            return api.bird.post('stripe/key', json_data=json_data)

        def get_user():
            return api.bird.get('user')

        def get_user_balance():
            return api.bird.get('user/balance')

        def push_user(platform='android', sandbox=False, token=None):
            json_data = {
                'platform': platform,
                'sandbox': sandbox,
                'token': token,
            }
            return api.bird.put('user/push', json_data=json_data)

        def update_user(agreed_at=None, birthdate=None, email=None, image_url=None, locale='en-US', name=None, phone=None, warehouse_id=None):
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
            return api.bird.put('user/update', json_data=json_data)

        def get_user_transacion_history(offset=0, limit=50):
            params = { 'offset': offset, 'limit': limit }
            return api.bird.get('user/transaction-history', params)

        def get_user_agreement(role='RIDER', partner_id=None):
            params = { 'role': role }
            if partner_id != None:
                params['partner_id'] = partner_id
            return api.bird.get('user-agreement', params)

        def get_merchant_by_user_id(id):
            params = { 'id': id }
            return api.bird.get('v1/merchant/byUserId', params)

        def get_coupon_by_coupon_id(coupon_ids=[]):
            json_data = { 'coupon_ids': coupon_ids }
            return api.bird.post('v1/merchant/coupon-extension/by-coupon-ids', json_data=json_data)

        def get_payment_reload_config(currency='eur'):
            params = { 'currency': currency }
            return api.bird.get('v1/payment/charge/reload-config', params)

        def get_payment_default_provider():
            return api.bird.get('v1/payment/provider/default')

        def get_payment_provider_token(user_id, kind='braintree'):
            json_data = { 'kind': kind, 'user_id': user_id }
            return api.bird.post('v1/payment/provider/token', json_data=json_data)

        def get_active_tutorial():
            return api.bird.get('v1/tutorial/active')

        def get_payment_method_list(user_id):
            params = { 'user_id': user_id }
            return api.bird.get('v3/payment-method/list', params)

        def zendesk_login(return_to="https://help.bird.co"):
            json_data = { 'return_to': return_to }
            return api.bird.post('zendesk/login', json_data=json_data)

    # this class is useless
    '''
    class birdplus:
        def get(endpoint):
            response = api.request.get('birdplus', f'api/v1/{endpoint}')
            return json.loads(response.content)

        def birdplus():
            return api.birdplus.get('bird-plus')

    class itemlease:
        def get(endpoint):
            response = api.request.get('itemlease', f'api/v1/itemlease/{endpoint}')
            return json.loads(response.content)

        def active_leases():
            return api.itemlease.get('active-leases')

    class localization:
        def get(endpoint, params):
            response = api.request.get('localization', f'api/v1/localization/{endpoint}', params=params)
            return json.loads(response.content)

        def ota_pull(project_id, modified_after=None):
            if modified_after == None:
                modified_after = api.request.build_timestamp()
            params = { 'bird_project_id': project_id, 'modified_after': modified_after }
            return api.localization.get('ota/pull', params)
    '''

    class rider:
        def get(endpoint, params=None):
            response = api.request.get('rider', f'/{endpoint}', params=params)
            return json.loads(response.content)

        def put(endpoint, params):
            response = api.request.put('rider', f'/{endpoint}', params=params)
            return json.loads(response.content)

        def get_all_long_term_rental(offset=0, limit=1, active=True):
            params = { 'offset': offset, 'limit': limit, 'active': active }
            return api.rider.get('long-term-rental/all', params)

        def get_active_multi_ride():
            return api.rider.get('multi-ride/active')

        def get_active_reservation():
            return api.rider.get('reservation/active')

        def last_ride_lock_compliance():
            return api.rider.get('ride/last-lock-compliance')

        def get_beginner_mode_options():
            return api.rider.get('rider-profile/ui/beginner-mode-options')

        # acceleration_level: 'advanced' or 'intermediate'
        def set_acceleration_level(acceleration_level):
            json_data = { 'acceleration_level': acceleration_level }
            return api.rider.put('rider-profile', json_data)

    def register(email):
        response = api.auth.get_tokens_from_email(email)
        if 'validation_required' not in response:
            print("Bird: Error: api.register: api.auth.get_tokens_from_email returned", response)
            return False
        if response['validation_required'] == False:
            api.set_tokens(response['tokens'])
            return True
        return False

    def send_email_code(email):
        response = api.auth.get_tokens_from_email(email)
        if 'validation_required' not in response:
            print("Bird: Error: api.send_email_code: api.auth.get_tokens_from_email returned", response)
            return False
        if response['validation_required'] == False:
            api.set_tokens(response['tokens'])
            print("Bird: Warning: api.send_email_code: You just created an account for", email)
            return False
        return True

    def login_from_email_code(email_code):
        response = api.auth.get_tokens_from_email_verification(email_code)
        if 'access' not in response:
            print("Bird: Error: api.login_from_email_code: api.auth.get_tokens_from_email_verification returned", response)
            return False
        api.set_tokens(response)
        return True

    def refresh_tokens():
        if api.tokens == None:
            print("Bird: Warning: api.refresh_tokens: You can't refresh tokens without initial token.")
            return False
        api.token = api.tokens['refresh']
        response = api.auth.get_tokens_from_refresh_token()
        if 'access' not in response:
            print("Bird: Error: api.refresh_session: api.auth.get_tokens_from_refresh_token returned", response)
            api.token = api.tokens['access']
            return False
        api.set_tokens(response)
        return True

    def login_from_tokens(tokens):
        api.set_tokens(tokens)
        api.refresh_tokens()
        return True

    def login(email_code=None, tokens=None):
        if email_code != None:
            return api.login_from_email_code(email_code)
        if tokens != None:
            return api.login_from_tokens(tokens)
        return False

    def sort_vehicles_by_distance(vehicle):
        return vehicle['distance']

    def get_nearby_vehicles(lat, lng, radius=1000.0, max_vehicles=None, session=None):
        api.set_position(lat, lng)
        response = api.bird.get_bird_nearby(api.lat, api.lng)
        if 'birds' not in response:
            if 'code' not in response:
                print("Bird: Error: api.get_nearby_vehicles: api.bird.get_bird_nearby returned", response)
                return None
            print("Bird: Error: api.get_nearby_vehicles: unknown error code", response['code'], ':', response)
            return None
        vehicles_list = []
        for infos in response['birds']:
            distance = geopy.distance.geodesic((infos['location']['latitude'], infos['location']['longitude']), (api.lat, api.lng)).m
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
            vehicles_final_list += [Vehicle(vehicle['infos'], session, distance=vehicle['distance'])]
        return vehicles_final_list


class Vehicle:
    def __init__(self, infos, session, distance=None):
        self.infos = infos
        self.distance = distance
        self.lat = infos['location']['latitude']
        self.lng = infos['location']['longitude']
        self.battery = infos['battery_level']
        self.name = infos['code'][:3] + 'XX'
        self.session = session

    def ring(self):
        if self.session != None:
            self.session.context.save_legacy()
            self.session.context.restore_session()
        response = api.bird.set_bird_chirp(self.infos['id'], alarm=False)
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
        self.location_header = None
        self.accuracy = 20.048999786376953
        self.altitude = 0.0
        self.heading = None
        self.mocked = False
        self.source = 'gps'
        self.speed = 0.0
        self.device_id = None
        self.tokens = None
        self.token = None

    def save_legacy(self):
        self.leg_lat = api.lat
        self.leg_lng = api.lng
        self.leg_location_header = api.location_header
        self.leg_accuracy = api.location.accuracy
        self.leg_altitude = api.location.altitude
        self.leg_heading = api.location.heading
        self.leg_mocked = api.location.mocked
        self.leg_source = api.location.source
        self.leg_speed = api.location.speed
        self.leg_device_id = api.device_id
        self.leg_tokens = api.tokens
        self.leg_token = api.token

    def restore_legacy(self):
        api.lat = self.leg_lat
        api.lng = self.leg_lng
        api.location_header = self.leg_location_header
        api.location.accuracy = self.leg_accuracy
        api.location.altitude = self.leg_altitude
        api.location.heading = self.leg_heading
        api.location.mocked = self.leg_mocked
        api.location.source = self.leg_source
        api.location.speed = self.leg_speed
        api.device_id = self.leg_device_id
        api.tokens = self.leg_tokens
        api.token = self.leg_token

    def save_session(self):
        self.lat = api.lat
        self.lng = api.lng
        self.location_header = api.location_header
        self.accuracy = api.location.accuracy
        self.altitude = api.location.altitude
        self.heading = api.location.heading
        self.mocked = api.location.mocked
        self.source = api.location.source
        self.speed = api.location.speed
        self.device_id = api.device_id
        self.tokens = api.tokens
        self.token = api.token

    def restore_session(self):
        api.lat = self.lat
        api.lng = self.lng
        api.location_header = self.location_header
        api.location.accuracy = self.accuracy
        api.location.altitude = self.altitude
        api.location.heading = self.heading
        api.location.mocked = self.mocked
        api.location.source = self.source
        api.location.speed = self.speed
        api.device_id = self.device_id
        api.tokens = self.tokens
        api.token = self.token

class Session:
    def __init__(self):
        self.context = context()

    def login(self, email_code=None, tokens=None):
        self.context.save_legacy()
        self.context.restore_session()
        result = api.login(email_code=email_code, tokens=tokens)
        self.context.save_session()
        self.context.restore_legacy()
        return result

    def get_nearby_vehicles(self, lat, lng, radius=300.0, max_vehicles=None):
        self.context.save_legacy()
        self.context.restore_session()
        result = api.get_nearby_vehicles(lat=lat, lng=lng, radius=radius, max_vehicles=max_vehicles, session=self)
        self.context.save_session()
        self.context.restore_legacy()
        return result
    

tokens = {"access": "eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiJlNzA3ZDExNC03ZTJhLTQ5N2QtOTdkZi1hYjc0YzRjYmU5MjgiLCJzdWIiOiI0YmQzZjUxZi0xYTk0LTQxN2EtYTVhMC00ZjkyNDA4ZWJiZjgiLCJuYmYiOjE2NTU3MTM2NTUsImV4cCI6MTY1NTgwMDA1NSwiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTY1NTcxMzY1NSwicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.Cpg4aZk_hiJ9IskIrxm-F_yk21j8wg-k1NSbQ5IpRyfYW6ozcCmAL2U0SOMZAa3rTgYdJCwh_LNEqWmz9ImrE0zG79NuCZPYwxBvxJen1X-fbrBsvAvSyl1_OtGKQ6lU8-uaaHeUZlSExbazmCYoxWc4tNrm2jrDrYxS-K7ULLjkLNry9NeNLnjnikRQzp8_cSOh9yLzStlU5AKqSLyOpnvybQ6Ii0Zv_Ij6I4g7NIZRDdQafv9SLpnfU2qbFd8J0yASNr5sgAjUhDSdM9AzNLJkpky4xjg6OQLFTX_kIUaAzQvCzR6HqS8F6F2Ok1KSOQhpbgo7ZJWwk1acqIbkdQcj_v_g8iwhgmom__aPWSzU7xWHZqTNrifqDhy6icxPbVh1H-M2HCGxsrZYoCT95I1JDTUYcG4iCW3O6XYdQcEO7lFDj4HGIbEPxoabUBsqxYXlLbg0PCieWjXv0yKqwC7STKeqqiWzt81AtsZc3dM425qv0681fgDJMqODAAy4Tpa-iVfPoErT2lJ_C4NLf8lzb-OS9OFMK8hKZxPjfMNOr2amJypoHGezOAfwx400zaR6GRKTDfqHWg9h-PHioRL1bbVXwnN6pFAcwBdJM0cAVvFd4Vq-_BJUjMB5JXDXJYfeNsZOs5JJ1CS0kLNWFTfbvTYMYeUJY-R8RUuXiCM", "refresh": "eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiJlNzA3ZDExNC03ZTJhLTQ5N2QtOTdkZi1hYjc0YzRjYmU5MjgiLCJzdWIiOiI0YmQzZjUxZi0xYTk0LTQxN2EtYTVhMC00ZjkyNDA4ZWJiZjgiLCJuYmYiOjE2NTU3MTM2NTUsImV4cCI6MTY3MTc4NDA1NSwiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTY1NTcxMzY1NSwicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.LLdO3-3SHBCGa1JX1-GXWuMejxPJAjOhLwYAgODqcm4wDN_NJuUnIX5Y-jTWwH8rfedRpW-TmMiOAIPlgMU0mWT2zRYOMKrPDI7Zpx_6kanyAcfGCkyp7QmQOneN3Oki0Ce-pUDQ75EK_vVRAcHmKKx0bdl55lT2m2nErpFR0fQ_UCSVG-BlHcJ5MlwbwIxNEI1WG-FEISRRYKCE7YbTohBi8noOHIoJcpwjIAO5X6w8OGoocoPp0ImczvYsSHMISZ78clngSI3llTGbmq5aExo59BSkqUuIjmkJWVu-abx9UeFuCdHpJYqEGLnQf5gavnUNFsprNd7BIA0f6W-SVs1R3_Tfn1jP5Ypnx2rWJl0U73pNtMFlq_Dv6X0u0Fltgs0R4TwbpONWb1r1epZKWotVjXEOxKQMNvJ5At1YTdzfNaiK6oV7mwUZpqrGrzJ0pc2dtI90MmpMXmtSzTWnDTwDw4x58YAcGVwRqe8_HQaNQFBcXRSeRLX4iKpBoT_N6zSdiZC4mld-14J07u-pG5_xG7YqlYsg2bk1Tn25xmbVICjh-7lHB8J_UWOdrKaDxP3Nt_81m1BIcSv_Q75jYqgK9BImLP1W1jyLkldiguWwxlGnOZqnrvpsrlyUvi_vB4IBKo82lSq4YEzwZuQel55G0Yvn1tdYD_FdJic-wRg"}
sess = Session()
sess.login(tokens=tokens)
vehicle = sess.get_nearby_vehicles(lat=50.846885386381636, lng=4.357265272965748, max_vehicles=10)[5]
print("Distance:", vehicle.distance)
#vehicle.ring()