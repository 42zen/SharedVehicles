# import the python libraries needed
import geopy.distance

# import the scrappers libraries needed
from scrappers import bird
from scrappers import bolt
from scrappers import bolt
from scrappers import lime
from scrappers import pony
from scrappers import tier
from scrappers import voi
#from scrappers import dott

# set the settings variable
DEBUG_SCAN = True

# build the services list
services_list = [
    {
        'name': 'Bolt',
        'module': bolt
    },
    {
        'name': 'Lime',
        'module': lime
    },
    {
        'name': 'Pony',
        'module': pony
    },
    {
        'name': 'Bird',
        'module': bird
    },
    {
        'name': 'Tier',
        'module': tier
    },
    {
        'name': 'Voi',
        'module': voi
    }
]

# sort dict list by distance key
def sort_by_distance(vehicle):
    return vehicle['distance']

# get the closest vehicle for a service
def get_closest_vehicle_for_service(service, lat, lng):
    # get the vehicles list
    vehicles = service['module'].get_vehicles(lat, lng)

    # check if the api is offline
    if vehicles == None:
        if DEBUG_SCAN == True:
            print("%s: Offline." % service['name'])
        return None
    
    # find the closest vehicle if any
    if vehicles != []:
        vehicles.sort(key=sort_by_distance)
        if DEBUG_SCAN == True:
            print("%s: ==> %.0f meters." % (vehicles[0]['brand'], vehicles[0]['distance']))
        return vehicles[0]
    
    # no vehicle found
    if DEBUG_SCAN == True:
        print("%s: No vehicles close to you." % service['name'])
    return None

# get the closest vehicle from all services
def get_closest_vehicle(lat, lng):
    # TODO: use multithreading

    # set the default closest vehicle
    closest_vehicle = None

    # find the closest vehicle from services list
    for service in services_list:
        service_closest_vehicle = get_closest_vehicle_for_service(service, lat, lng)
        if service_closest_vehicle != None:
            if closest_vehicle == None or service_closest_vehicle['distance'] < closest_vehicle['distance']:
                closest_vehicle = service_closest_vehicle

    # return the closest vehicle
    return closest_vehicle

# prepare to ring a specified vehicle faster
def prepare_ring_vehicle(vehicle):
    if vehicle['brand'] == 'Bolt':
        return True
    elif vehicle['brand'] == 'Lime':
        lime.get_vehicles(vehicle['lat'], vehicle['lng'])
        return True
    elif vehicle['brand'] == 'Tier':
        tier.get_vehicles(vehicle['lat'], vehicle['lng'])
        return True
    return False

# ring a specified vehicle
def ring_vehicle(vehicle, prepared=False):
    if vehicle['brand'] == 'Bolt':
        bolt.ring_vehicle(vehicle['infos'])
        return True
    elif vehicle['brand'] == 'Lime':
        lime.ring_vehicle(vehicle['infos'], position_is_set=prepared)
        return True
    elif vehicle['brand'] == 'Tier':
        tier.ring_vehicle(vehicle['infos'], position_is_set=prepared)
        return True
    return False
