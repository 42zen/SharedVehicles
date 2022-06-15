import requests
import json
import geopy.distance


"""
Informations used by the API
"""
API_HOST = 'api.voiapp.io'

DEVICE_ID = '792c4d6d2fd31aa8'
DEVICE_OS = 'Android'
DEVICE_OS_API_VERSION = '28'
DEVICE_MODEL = 'AOSP on IA Emulator'
DEVICE_MANUFACTURER = 'Google'

APP_NAME = 'Rider'
APP_VERSION = '3.127.1'
APP_CLIENT = 'okhttp/4.9.1'

TOKEN_FILENAME = 'tokens/voi.tokens'


"""
A class to manage API calls
"""
class api:

    """
    Send a request to the API
    """
    def request(endpoint, json_data=None, params=None, access_token=None):
        # build the headers
        headers = {
            'Host': API_HOST,
            'X-Device-Id': DEVICE_ID,
            'X-App-Version': APP_VERSION,
            'X-Os': DEVICE_OS,
            'X-Os-Version': DEVICE_OS_API_VERSION,
            'Model': DEVICE_MODEL,
            'Brand': DEVICE_MANUFACTURER.lower(),
            'Manufacturer': DEVICE_MANUFACTURER,
            'X-App-Name': APP_NAME,
            'X-Request-Id': 'cd8687cd-d6bf-4414-8b4f-5de6978394e4',
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': APP_CLIENT
        }

        # add the access token if needed
        if access_token != None:
            headers['X-Access-Token'] = access_token

        # build the url
        url = f'https://{API_HOST}/{endpoint}'

        # send the request
        if access_token == None:
            response = requests.post(url, headers=headers, json=json_data, params=params)
        else:
            response = requests.get(url, headers=headers, json=json_data, params=params)

        # return the response
        return response
    
    # TODO: def get_zones()

    """
    Get the shared vehicles list
    """
    def get_vehicles(lat, lng, tokens):
        # TODO: get_vehicles from position
        return None

    """
    Get the shared vehicles list from zone id
    """
    def get_vehicles_from_zone_id(zone_id, tokens):
        # build the params
        params = {
            'zone_id': zone_id
        }

        # send the request
        response = api.request('v2/rides/vehicles', params=params, access_token=tokens['accessToken'])

        # return the response
        return response


"""
A class to manage authentification
"""
class auth_api:

    """
    Get an authentification token from a google code
    """
    def get_auth_token_from_google(code):
        # build the json data
        json_data = {
            'authorizationCode': code,
        }

        # send the request
        response = api.request('v1/auth/google/signin', json_data=json_data)

        # return the authentification token
        return json.loads(response.content)['authToken']

    # TODO: def get_auth_token_from_phone(phone_number):

    """
    Get tokens from an authentification token
    """
    def get_tokens(auth_token):
        # build the json data
        json_data = {
            'authenticationToken': auth_token,
        }

        # send the request
        response = api.request('v1/auth/session', json_data=json_data)

        # return the tokens
        return json.loads(response.content)

    """
    Save the current voi API tokens
    """
    def save_tokens(tokens, tokens_filename=TOKEN_FILENAME):
        # open the tokens file
        tokens_file = open(tokens_filename, 'w')

        # save the json content in file
        json.dump(tokens, tokens_file)

        # close the tokens file
        tokens_file.close()

    """
    Load the current voi API tokens
    """
    def load_tokens(tokens_filename=TOKEN_FILENAME):
        # create the tokens values
        tokens = None

        # open the tokens file
        tokens_file = None
        try:
            tokens_file = open(tokens_filename, 'r')
        except FileNotFoundError:
            pass

        # save and close the file if needed
        if tokens_file != None:
            # save the json content in file
            tokens = json.load(tokens_file)

            # close the tokens file
            tokens_file.close()

        # return the tokens loaded if any
        if tokens != None:
            return tokens

        # there is no tokens to load
        return None

"""
Login to the Voi API
"""
def login(google_code=None, tokens_filename=TOKEN_FILENAME, load_tokens_from_file=True):
    # load the current tokens if any
    if tokens_filename != None and load_tokens_from_file == True:
        tokens = auth_api.load_tokens(tokens_filename)
        if tokens != None:
            return tokens

    # authenticate using google code if any
    if google_code != None:
        auth_token = auth_api.get_auth_token_from_google(google_code)
        tokens = auth_api.get_tokens(auth_token)

    # check if we have the tokens
    if tokens == None:
        return False

    # save the tokens if needed
    if tokens_filename != None:
        auth_api.save_tokens(tokens, tokens_filename)

    # we are logged
    return tokens

"""
Check the vehicle model for any API changes

Current Model:
"""
def check_vehicle_model(vehicle):
    # TODO: check_vehicle_model
    pass

"""
Get the shared vehicles list
"""
def get_vehicles(lat, lng, radius=None, zone_id=None, tokens=None, tokens_filename=TOKEN_FILENAME, load_tokens_from_file=True, refresh_token=True):
    # load the current tokens if any
    if tokens == None and tokens_filename != None and load_tokens_from_file == True:
        tokens = auth_api.load_tokens(tokens_filename)
        if tokens == None:
            return None

    # get the vehicles list
    response = None
    if lat != None and lng != None:
        response = api.get_vehicles(lat, lng, tokens)
    elif zone_id != None:
        response = api.get_vehicles_from_zone_id(zone_id, tokens)
    if response == None:
        return None

    # refresh the token if needed
    if response.status_code == 401:
        if refresh_token == True:
            tokens = auth_api.get_tokens(tokens['authenticationToken'])
            if tokens_filename != None:
                auth_api.save_tokens(tokens, tokens_filename)
            return get_vehicles(zone_id=zone_id, tokens_filename=tokens_filename)
        else:
            return False

    # check the response status code
    if response.status_code != 200:
        print('Error: Voi: get_vehicles: Invalid status code: %i.' % response.status_code)
        return None

    # parse the response content
    response = json.loads(response.content)

    # TODO: parse vehicles list
    print(json.dumps(response, sort_keys=True, indent=4))

    # build the vehicles list
    vehicles_list = []
    for vehicle_info in response['data']['attributes']['bikes']:
        check_vehicle_model(vehicle_info)
        vehicle_lat = vehicle_info['attributes']['latitude']
        vehicle_lng = vehicle_info['attributes']['longitude']
        dist = geopy.distance.geodesic((lat, lng), (vehicle_lat, vehicle_lng)).m
        if radius == None or dist <= radius:
            vehicle = {
                'brand': 'Voi',
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
A class to manage accounts
"""
class Account:

    def __init__(self):
        self.tokens_filename = None
        self.tokens = None
        self.lat = None
        self.lng = None

    """
    Login to the bird API
    """
    def login(self, google_code=None, tokens_filename=None):
        self.tokens_filename = tokens_filename
        self.tokens = login(google_code=google_code, tokens_filename=tokens_filename)
        if self.tokens == False:
            self.tokens = None
            return False
        return True

    """
    Get the shared vehicles list
    """
    def get_vehicles(self, lat, lng, radius=None):
        # save the current position
        self.lat = lat
        self.lng = lng

        # use the current tokens
        tokens = self.tokens

        # check if you need to login
        if tokens == None:
            print("Error: Voi: You need to login.")
            return None

        # get the vehicles list
        response = get_vehicles(lat, lng, radius=radius, tokens=tokens, tokens_filename=None, refresh_token=False)
        if response == None:
            response = []

        # refresh the token if needed
        if response == False:
            self.tokens = auth_api.get_tokens(tokens['authenticationToken'])
            if self.tokens_filename != None:
                auth_api.save_tokens(tokens, self.tokens_filename)
            return self.get_vehicles(lat, lng, radius=radius)

        # return the response
        return response