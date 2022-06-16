import requests
import json
import geopy.distance


"""
Informations used by the API
"""
API_HOST = 'prod.birdapp.com'

DEVICE_OS_NAME = 'Android'
DEVICE_OS_VERSION = '9'
DEVICE_LANG = 'en'
DEVICE_REGION = 'US'
DEVICE_ID = '5f0f6ad45d14c714'
DEVICE_MODEL = 'AOSP on IA Emulator'
DEVICE_ARCH = 'generic_x86_arm'

APP_NAME = 'bird'
APP_TYPE = 'rider'
APP_VERSION = '4.189.0.9'

TOKENS_FILENAME = 'tokens/bird.tokens'


"""
A class to manage API calls
"""
class api:

    """
    Send a request to the API
    """
    def request(endpoint, json_data=None, token=None, api='bird', params=None, lat=None, lng=None, device_id=DEVICE_ID):
        # build the hostname
        host = f'api-{api}.{API_HOST}'

        # build the headers
        headers = {
            'Host': host,
            'App-Version': APP_VERSION,
            'Accept-Language': f'{DEVICE_LANG}-{DEVICE_REGION},{DEVICE_LANG}',
            'Bird-Device-Id': device_id,
            'Battery-Level': '100',
            'Bluetooth-State': 'disabled',
            'Carrier-Name': DEVICE_OS_NAME,
            #'Client-Time': '2022-06-06T14:34:33.592+02:00',
            'Connection-Type': 'unknown',
            'Device-Model': DEVICE_MODEL,
            'Device-Name': DEVICE_ARCH,
            'Device-Region': DEVICE_REGION,
            'Device-Language': DEVICE_LANG,
            'Device-Id': device_id,
            #'Location': '{"accuracy":603.0,"altitude":null,"heading":null,"latitude":37.4220005,"longitude":-122.0839996,"mocked":false,"source":"gps","speed":null,"timestamp":"2022-06-06T14:32:06.205+02:00"}',
            'Mobile-Network-Generation': 'unknown',
            'Os-Version': DEVICE_OS_VERSION,
            'Platform': DEVICE_OS_NAME.lower(),
            'User-Agent': f'{DEVICE_OS_NAME} - {DEVICE_OS_VERSION}',
            'App-Name': APP_NAME,
            'App-Type': APP_TYPE,
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'close'
        }

        # add the auth header if needed
        if token != None:
            headers['Authorization'] = f'Bearer {token}'

        # add the location header if needed
        if api == 'bird':
            headers['Location'] = '{' + f'"latitude":{lat},"longitude":{lng}' + '}'

        # build the api path
        api_path = 'api/v1/auth'
        if api == 'bird':
            api_path = 'bird'

        # send the request
        url = f'https://{host}/{api_path}/{endpoint}'
        if api == 'auth':
            response = requests.post(url, headers=headers, json=json_data, params=params)
        else:
            response = requests.get(url, headers=headers, json=json_data, params=params)

        # return the response
        return response

    """
    Get the shared vehicles list
    """
    def get_vehicles(lat, lng, access_token, radius=5000.0):
        # build the params
        params = {
            'latitude': lat,
            'longitude': lng,
            'radius': radius
        }

        # send the request
        response = api.request('nearby', params=params, token=access_token, lat=lat, lng=lng)

        # return the response
        return response


"""
A class to manage authentification
"""
class auth_api:

    """
    Send a code to an email
    """
    def send_code_to_email(email, device_id=DEVICE_ID):
        # build the json data
        json_data = {
            'email': email,
        }

        # send the request
        response = api.request('email', json_data=json_data, api='auth', device_id=device_id)

        # check the response status code
        if response.status_code != 200:
            print('Error: Bird: send_code_to_email: Invalid status code: %i.' % response.status_code)
            return None

        # return the parsed response
        return json.loads(response.content)

    """
    Get an access token and a refresh token from a code
    """
    def get_tokens_from_code(code):
        # build the json data
        json_data = {
            'token': code,
        }

        # send the request
        response = api.request('magic-link/use', json_data=json_data, api='auth')

        # check if the code is invalid
        if response.status_code == 404:
            return None

        # check if the code is already entered
        if response.status_code == 400:
            return None

        # check the response status code
        if response.status_code != 200:
            print('Error: Bird: get_tokens_from_code: Invalid status code: %i.' % response.status_code)
            return None

        # return the parsed response
        return json.loads(response.content)

    """
    Get an access token and a refresh token from a refresh token
    """
    def refresh_tokens(refresh_token):
        # send the request
        response = api.request('refresh/token', token=refresh_token, api='auth')

        # check the response status code
        if response.status_code != 200:
            print('Error: Bird: refresh_tokens: Invalid status code: %i.' % response.status_code)
            return None

        # return the parsed response
        return json.loads(response.content)

    """
    Save the current bird API tokens
    """
    def save_tokens(tokens, tokens_filename=TOKENS_FILENAME):
        # open the tokens file
        tokens_file = open(tokens_filename, 'w')

        # save the json content in file
        json.dump(tokens, tokens_file)

        # close the tokens file
        tokens_file.close()


    """
    Load the current bird API tokens
    """
    def load_tokens(tokens_filename=TOKENS_FILENAME):
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
A class to manage analytics
"""


"""
Login to the bird API using command line inerface
"""
def cli_login(email=None, code=None, tokens_filename=TOKENS_FILENAME):
    # check if we need to send a code
    if email == None and code == None:
        # ask the user for an email
        email = input("Enter your email: ")

    # send a code to an email if needed
    if code == None:
        response = auth_api.send_code_to_email(email)

    # check if we need to validate the code
    if code != None or response['validation_required'] == True:
        if code == None:
            max_try = 3
            while max_try > 0:
                # ask the user for the code received
                code = input("Enter the code received by email: ")

                # get the tokens from the code
                tokens = auth_api.get_tokens_from_code(code)

                # check if the code is valid
                if tokens == None:
                    print("Invalid code entered.")
                else:
                    break

                # decrease try count
                max_try -= 1

            # check if you don't have the code
            if max_try == 0:
                print("Error: Maximum try exceeded for email code.")
                return None
        else:
            # get the tokens from the code
            tokens = auth_api.get_tokens_from_code(code)

            # check if the code is valid
            if tokens == None:
                print("Error: Invalid code entered.")
                return None
    else:
        tokens = response['tokens']

    # save the tokens in file if needed
    if tokens_filename != None:
        auth_api.save_tokens(tokens, tokens_filename)
        
    # return the tokens received
    return tokens

"""
Register to the bird API using command line inerface
"""
def cli_register(email=None, code=None, tokens_filename=TOKENS_FILENAME):
    return cli_login(email=email, code=code, tokens_filename=tokens_filename)

"""
Login to the bird API
"""
def login(email=None, code=None, tokens_filename=TOKENS_FILENAME, load_tokens_from_file=True):
    # load the current tokens if needed
    if tokens_filename != None and load_tokens_from_file == True:
        tokens = auth_api.load_tokens(tokens_filename)
        if tokens != None:
            return tokens

    # send a code to an email if needed
    if code == None:
        response = auth_api.send_code_to_email(email)
        if response['validation_required'] == False:
            tokens = response['tokens']
        
    # get the tokens from the code
    if tokens == None:
        tokens = auth_api.get_tokens_from_code(code)

    # check if the code is valid
    if tokens == None:
        print("Error: Invalid code entered.")
        return False

    # save the tokens in file if needed
    if tokens_filename != None:
        auth_api.save_tokens(tokens, tokens_filename)
            
    # return the tokens received
    return tokens

"""
Register to the bird API
"""
def register(email=None, code=None, tokens_filename=TOKENS_FILENAME):
    return login(email=email, code=code, tokens_filename=tokens_filename, load_tokens_from_file=False)

"""
Check the vehicle model for any API changes

Current Model:
{
    "area_key": "92A928A295D01D313E027B4667E6B6F4",
    "battery_level": 41,
    "captive": false,
    "code": "7AC\u2022\u2022",
    "estimated_range": 10701,
    "has_helmet": false,
    "id": "c562f844-4484-44b2-bc1c-80a196773d85",
    "model": "rf",
    "partner_id": "c4285d50-5ef4-495a-b9cb-33522bfc0a61",
    "vehicle_class": "scooter",
    "location": {
        "latitude": 50.84673666666666,
        "longitude": 4.356818333333334
    }
}
"""
def check_vehicle_model(vehicle):
    # TODO: check_vehicle_model
    pass

"""
Get the shared vehicles list
"""
def get_vehicles(lat, lng, radius=None, tokens=None, tokens_filename=TOKENS_FILENAME, load_tokens_from_file=True, refresh_token=True):
    # load the current tokens if any
    if tokens == None and tokens_filename != None and load_tokens_from_file == True:
        tokens = auth_api.load_tokens(tokens_filename)

    # login if needed
    if tokens == None:
        print("You need to log-in to your Bird account.")
        tokens = login(tokens_filename=tokens_filename)

    # send the request
    response = api.get_vehicles(lat, lng, tokens['access'])

    # refresh the tokens if needed
    if response.status_code == 401:
        if refresh_token == True:
            tokens = auth_api.refresh_tokens(tokens['refresh'])
            if tokens_filename != None:
                auth_api.save_tokens(tokens, tokens_filename)
                return get_vehicles(lat, lng, radius=radius, tokens_filename=tokens_filename)
            return get_vehicles(lat, lng, radius=radius, tokens=tokens, tokens_filename=tokens_filename, load_tokens_from_file=False)
        else:
            return False

    # check the response status code
    if response.status_code != 200:
        print('Error: Bird: get_vehicles: Invalid status code: %i.' % response.status_code)
        print(response.content)
        return None

    # parse the response content
    response = json.loads(response.content)

    # build the vehicles list
    vehicles_list = []
    for vehicle_info in response['birds']:
        check_vehicle_model(vehicle_info)
        vehicle_lat = vehicle_info['location']['latitude']
        vehicle_lng = vehicle_info['location']['longitude']
        dist = geopy.distance.geodesic((lat, lng), (vehicle_lat, vehicle_lng)).m
        if radius == None or dist <= radius:
            vehicle = {
                'brand': 'Bird',
                'lat': vehicle_lat,
                'lng': vehicle_lng,
                'battery': vehicle_info['battery_level'],
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
        self.tokens = None
        self.tokens_filename = None
        self.lat = None
        self.lng = None

    """
    Login to the bird API using command line inerface
    """
    def cli_login(self, email=None, code=None, tokens_filename=None):
        self.tokens_filename = tokens_filename
        self.tokens = cli_login(email=email, code=code, tokens_filename=tokens_filename)
        if self.tokens == None:
            return False
        return True

    """
    Register to the bird API using command line inerface
    """
    def cli_register(self, email=None, code=None, tokens_filename=None):
        self.tokens_filename = tokens_filename
        self.tokens = cli_register(email=email, code=code, tokens_filename=tokens_filename)
        if self.tokens == None:
            return False
        return True

    """
    Login to the bird API
    """
    def login(self, email=None, code=None, tokens_filename=None, load_tokens_from_file=True):
        self.tokens_filename = tokens_filename
        self.tokens = login(email=email, code=code, tokens_filename=tokens_filename, load_tokens_from_file=load_tokens_from_file)
        if self.tokens == False:
            self.tokens = None
            return False
        return True

    """
    Register to the bird API
    """
    def register(self, email=None, code=None, tokens_filename=None):
        self.tokens_filename = tokens_filename
        self.tokens = register(email=email, code=code, tokens_filename=tokens_filename)
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
            return None

        # get the vehicles list
        response = get_vehicles(lat, lng, radius=radius, tokens=tokens, tokens_filename=self.tokens_filename, refresh_token=False)

        # refresh the token if needed
        if response == False:
            self.tokens = auth_api.refresh_tokens(self.tokens['refresh'])
            if self.tokens_filename != None:
                auth_api.save_tokens(tokens, self.tokens_filename)
            return self.get_vehicles(lat, lng, radius=radius)

        # return the response
        return response
