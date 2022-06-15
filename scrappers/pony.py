import requests
from websocket import create_connection
import json
import datetime
import geopy.distance

"""
Informations used by the API
"""
API_HOST = 'core.getapony.com'
API_WS_HOST = 'pony-bikes-f8cf9.firebaseio.com'
API_WS_ENDPOINT = '.ws?ns=pony-bikes-f8cf9&v=5'

DEVICE_OS = 'Android'
DEVICE_API_VERSION = '28'

APP_NAME = 'pony'
APP_BUILD_VERSION = '1462'
APP_VERSION = f'2.13.3_{APP_BUILD_VERSION}'

class api:

    """
    Get the region from a position
    """
    def get_region(lat, lng):
        # build the headers
        headers = {
            'Host': API_HOST,
            'Accept': 'application/json',
            'Pony-Seqno': '0',
            'User-Agent': DEVICE_OS,
            'App_name': APP_NAME,
            'Platform': DEVICE_OS,
            'Os_version': DEVICE_API_VERSION,
            'Build_number': APP_BUILD_VERSION,
            'App_version': APP_VERSION,
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'close'
        }

        # build the params
        json_data = {
            'latitude': lat,
            'longitude': lng,
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        }

        # send the request
        response = requests.post(f'https://{API_HOST}/regions', headers=headers, json=json_data)

        # return the parsed response
        return json.loads(response.content)

    """
    Get the shared vehicles list
    """
    def get_vehicles(region):
        # connect to the websocket server
        ws = create_connection(f'wss://{API_WS_HOST}/{API_WS_ENDPOINT}')

        # receive the welcome message
        result =  ws.recv()

        # request the full vehicles list
        result =  ws.send("{\"t\":\"d\",\"d\":{\"a\":\"q\",\"r\":1,\"b\":{\"p\":\"rest\/bicycles\",\"q\":{\"i\":\"region\",\"ep\":\"" + region + "\",\"sp\":\"" + region + "\"},\"t\":1,\"h\":\"\"}}}")
        result =  ws.send("{\"t\":\"d\",\"d\":{\"a\":\"q\",\"r\":2,\"b\":{\"p\":\"rest\/scooters\",\"q\":{\"i\":\"region\",\"ep\":\"" + region + "\",\"sp\":\"" + region + "\"},\"t\":1,\"h\":\"\"}}}")
        result =  ws.send("{\"t\":\"d\",\"d\":{\"a\":\"q\",\"r\":3,\"b\":{\"p\":\"rest\/ebikes\",\"q\":{\"i\":\"region\",\"ep\":\"" + region + "\",\"sp\":\"" + region + "\"},\"t\":1,\"h\":\"\"}}}")

        # receive the full vehicles list
        full_result = ''
        result =  ws.recv()
        found = [False, False, False]
        while result:
            if result == "{\"t\":\"d\",\"d\":{\"r\":1,\"b\":{\"s\":\"ok\",\"d\":{}}}}":
                found[0] = True
            elif result == "{\"t\":\"d\",\"d\":{\"r\":2,\"b\":{\"s\":\"ok\",\"d\":{}}}}":
                found[1] = True
            elif result == "{\"t\":\"d\",\"d\":{\"r\":3,\"b\":{\"s\":\"ok\",\"d\":{}}}}":
                found[2] = True
            else:
                full_result += result
            if found == [True, True, True]:
                break
            result =  ws.recv()

        # fix the vehicles list format
        full_result = str(full_result)
        pos = full_result.find('{')
        if pos != -1:
            full_result = full_result[pos:]

        # close the websocket connection
        ws.close()

        # return the parsed response
        return json.loads(full_result.encode("utf-8"))

"""
Check the vehicle model for any API changes

Current Model:
"S000958": {
    "batteryAlertSentTo": "",
    "batteryLevel": 0.01,
    "charging": true,
    "checkedoutForOPS": true,
    "created_at": "2022-04-20T10:33:18",
    "currentSpeedMode": "2",
    "defaultSpeedMode": 2,
    "ghost": false,
    "iotCode": "867584031296234",
    "iotType": "electisan",
    "isCheckedoutForGig": false,
    "lastHeartBeatUpdate": "2022-05-27T02:29:47.056Z",
    "lastTelemetryUpdate": "2022-05-27T02:25:36.459Z",
    "locked": true,
    "macAddress": "F8:6B:DA:C6:03:0A",
    "moduleId": "864431042548489",
    "needsCollection": false,
    "online": false,
    "position": {
        "latitude": 50.895531,
        "longitude": 4.247002,
        "timestamp": "2022-03-27T19:10:51.000Z"
    },
    "reason": "0",
    "region": "Brussels",
    "status": "HIDDEN",
    "updated_at": "2022-05-27T02:31:50Z",
    "vehicleCode": "867584031296234",
    "vehicle_model": "es400a",
    "vehicle_type": "scooter"
}
"""
def check_vehicle_model(vehicle):
    # TODO: check_vehicle_model
    pass

"""
Get the shared vehicles list
"""
def get_vehicles(lat=None, lng=None, region=None, radius=None):
    # find the region if needed
    if lat != None and lng != None and region == None:
        region = api.get_region(lat, lng)['region']
    elif region == None:
        return None

    # request the vehicles list from the api
    response = api.get_vehicles(region)
    if response == None:
        return None

    # build the vehicles list
    vehicles_list = []
    data = response['d']['b']['d']
    for vehicle_field in data:
        vehicle_info = data[vehicle_field]
        vehicle_info['id'] = vehicle_field
        #print(vehicle_info)
        check_vehicle_model(vehicle_info)
        if 'position' not in vehicle_info:
            continue
        if 'batteryLevel' not in vehicle_info:
            battery = -1
        else:
            battery = int(vehicle_info['batteryLevel'] * 100)
        vehicle_lat = vehicle_info['position']['latitude']
        vehicle_lng = vehicle_info['position']['longitude']
        dist = geopy.distance.geodesic((lat, lng), (vehicle_lat, vehicle_lng)).m
        if radius == None or dist <= radius:
            vehicle = {
                'brand': 'Pony',
                'lat': vehicle_lat,
                'lng': vehicle_lng,
                'battery': battery,
                'distance': dist,
                'infos': vehicle_info
            }
            vehicles_list += [vehicle]

    # return the vehicle list
    return vehicles_list
