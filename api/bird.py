import requests
import json

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

    access_token =  'Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiI4YTA2MDJlZS00ZDg3LTQ2ZjItYjg1Ni0xMG' \
                    'NlM2M5OTFiMGUiLCJzdWIiOiJmODhiNzIxOS1kODk5LTQxOGYtODMzZi05M2E0MGJiZDQyMzMi' \
                    'LCJuYmYiOjE2NTUzNjczNDIsImV4cCI6MTY1NTQ1Mzc0MiwiYXVkIjoiYmlyZC5zZXJ2aWNlcy' \
                    'IsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTY1NTM2NzM0Miwicm9sZXMiOlsiVVNFUiJdLCJh' \
                    'cHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMi' \
                    'J9.BPNlT6yn7NtWsKe9NSJD4nDmYDjU0e0sB1HRX_i0GoRtRv9vlr0azra4R_u6xTifTpfFuC_' \
                    'Eyz2W248duTpPR7PoQ2P65MzQzrLz7Ko7P-BYHRxbrWJreAk-3KV_GQrcSPyHITwokeS5WlzfE' \
                    'hW8gPymdGWozCYw0D6kaTzZ0pn8oNxxHmwzJiQMQHyDfRpMbBStDLyIOtWVd4Lur2zeXm_4y9r' \
                    '3acs6CP6E1CkUjg2qUfeS6-dffhw13TpXiMSP9sfd2M0b4gMjszztDY3rELLQIjEuQxVdKwNYn' \
                    '8fTzdYTeh_TdJInA05nBNq3xkAS-fePNy7fMn-kd6fFcM6g9neM4WQc8u9yTjRcMFLCKTny9qo' \
                    '7JpgmpoqYwd4bzpy-LSHFzbk5VMYTLaT63aZbTBTr2nnzCJgIBouSLGvAf_omeaxn1HUoY-9Ll' \
                    'h3okBSwZsjDwQG2UrWPrdAccjAkDypJgBzrmWldGeyr9iQLzYkhKTRMKCQotvAuaQdXi3FV9YY' \
                    'wF8I2SgHzZuX2TeI2u3vfdZZOCG-XC5n0iz7zATa8Xn7C27bFLUOkTulA2PM62R9pDYW6rB3sN' \
                    'QSxlyIdqqZWS7lpTEcjal7cRdE6ShZHVTxKLOj4_kfdQWJW0kHx1HN7ueXaACCfgQYu5WvnPxA' \
                    'eQqDE-h20mA0_Jhcz0go'

    device_id = '5f0f6ad45d14c714'

    lat = 0.0
    lng = 0.0

    loc_accuracy = 20.0
    loc_altitude = 0.0
    loc_heading = None
    loc_mocked = False
    loc_source = "gps"
    loc_speed = 0.0

    def set_access_token(access_token):
        api.access_token = access_token

    def set_device_id(device_id):
        api.device_id = device_id

    def set_position(lat, lng):
        api.lat = lat
        api.lng = lng

    def set_location(accuracy=20.048999786376953, altitude=0.0, heading=None, mocked=False, source="gps", speed=0.0):
        api.loc_accuracy = accuracy
        api.loc_altitude = altitude
        api.loc_heading = heading
        api.loc_mocked = mocked
        api.loc_source = source
        api.loc_speed = speed

    class request:
        def build_headers(api_name):
            location = {
                    "accuracy": api.loc_accuracy,
                    "altitude": api.loc_altitude,
                    "heading": api.loc_heading,
                    "latitude": api.lat,
                    "longitude": api.lng,
                    "mocked": api.loc_mocked,
                    "source": api.loc_source,
                    "speed": api.loc_speed,
                    #"timestamp": "2022-06-16T10:41:14.000+02:00" # TODO
            }
            headers = {
                'Host': f'api-{api_name}.prod.birdapp.com',
                'App-Version': APP_VERSION,
                'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION},{DEVICE_LANG}',
                'Bird-Device-Id': api.device_id,
                'Battery-Level': '100',
                'Bluetooth-State': 'disabled',
                'Carrier-Name': DEVICE_OS,
                #'Client-Time': '2022-06-16T10:41:14.910+02:00', # TODO
                'Connection-Type': 'unknown',
                'Device-Model': DEVICE_MODEL,
                'Device-Name': DEVICE_ARCH,
                'Device-Region': DEVICE_REGION,
                'Device-Language': DEVICE_LANG,
                'Device-Id': api.device_id,
                'Location': json.dumps(location, separators=(',', ':')),
                'Mobile-Network-Generation': 'unknown',
                'Os-Version': DEVICE_OS_VERSION,
                'Platform': DEVICE_OS.lower(),
                'User-Agent': f'{DEVICE_OS} - {DEVICE_OS_VERSION}',
                'App-Name': APP_NAME,
                'App-Type': APP_TYPE,
                'Authorization': api.access_token,
                'Content-Type': 'application/json; charset=UTF-8'
            }
            return headers

        def request(api_name, endpoint, params=None, json_data=None, req=requests.get):
            headers = api.request.build_headers(api_name)
            url = f'https://api-{api_name}.prod.birdapp.com/{endpoint}'
            if req != requests.get:
                return req(url, headers=headers, params=params, json_data=json_data)
            return req(url, headers=headers, params=params)

        def get(api_name, endpoint, params=None):
            return api.request.request(api_name, endpoint, params=params)

        def post(api_name, endpoint, params=None, json_data=None):
            return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=requests.post)

        def put(api_name, endpoint, params=None, json_data=None):
            return api.request.request(api_name, endpoint, params=params, json_data=json_data, req=requests.put)

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

    class auth:
        def post(endpoint, json_data=None):
            response = api.request.post('auth', f'api/v1/auth/{endpoint}', json_data=json_data)
            return json.loads(response.content)

        def get_tokens_from_email(email):
            json_data = { 'email': email }
            return api.auth.post('email', json_data=json_data)

        def get_tokens_from_email_verification(code):
            json_data = { 'token': code }
            return api.auth.post('magic-link/use', json_data=json_data)

        def get_tokens_from_refresh_token(code):
            return api.auth.post('refresh/token')

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

        def get_area_nearby(lat, lng, radius='5000.0', include_merged=True):
            params = {
                'latitude': lat,
                'longitude': lng,
                'radius': radius,
                'include_merged': include_merged
            }
            return api.bird.get('area/nearby', params=params)

        def set_bird_chirp(bird_id, alarm=False):
            json_data = {
                'alarm': alarm,
                'bird_id': bird_id
            }
            return api.bird.put('bird/chirp', json_data=json_data)

        def set_bird_missing(bird_id, request_role='rider'):
            json_data = {
                'bird_id': bird_id,
                'request_role': request_role
            }
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

        def get_stripe_key(api_version='2020-03-02'): # '2017-06-05' is also something
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
            # TODO: if modified_after == None: modified_after = current_time
            # modified_after sample: '2022-05-14T00:00:06.754+02:00'
            params = { 'bird_project_id': project_id }
            if modified_after != None:
                params['modified_after'] = modified_after
            return api.localization.get('ota/pull', params)

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

        def set_acceleration_level(acceleration_level):
            if acceleration_level != 'advanced' and acceleration_level != 'intermediate':
                print(f'Error: Unknown acceleration level {acceleration_level}.')
                return None
            json_data = { 'acceleration_level': acceleration_level }
            return api.rider.put('rider-profile', json_data)

        def get_beginner_mode_options():
            return api.rider.get('rider-profile/ui/beginner-mode-options')
