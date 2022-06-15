# import the scrappers libraries needed
from scrappers import bird
from scrappers import bolt
from scrappers import cityscoot
from scrappers import cooltra
from scrappers import felyx
from scrappers import gosharing
from scrappers import lime
from scrappers import nextbike
from scrappers import pony
from scrappers import poppy
from scrappers import superpedestrian
from scrappers import tier
from scrappers import villo
from scrappers import voi

# build the brussel services list
bxl_services_list = [
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

# set the brussel position
bxl_lat = 50.846885386381636
bxl_lng = 4.357265272965748

# test all brussels services APIs
for service in bxl_services_list:
    print("Testing the %s API..." % service['name'], end='', flush=True)
    vehicles_list = service['module'].get_vehicles(bxl_lat, bxl_lng)
    if vehicles_list != None:
        vehicles_count = len(vehicles_list)
    else:
        vehicles_count = 0
    if vehicles_count > 0:
        print("Online: %i vehicles close to Brussels." % vehicles_count)
    else:
        print("Offline.")

# set the bordeaux position
bdx_lat = 44.837789
bdx_lng = -0.57918

# test the cityscoot api
print("Testing the CityScoot API...", end='', flush=True)
r = cityscoot.get_vehicles(4)
if r != None:
    vehicles_count = len(r['data']['scooters'])
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles close to Paris." % vehicles_count)

# test the cooltra api
print("Testing the Cooltra API...", end='', flush=True)
r = cooltra.get_vehicles('paris')
if r != None:
    vehicles_count = len(r)
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles close to Paris." % vehicles_count)


# test the felyx api
print("Testing the Felyx API...", end='', flush=True)
r = felyx.get_vehicles(bxl_lat, bxl_lng, radius=1000000)
if r != None:
    vehicles_count = len(r)
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles close to Brussels." % vehicles_count)

# test the gosharing api
print("Testing the GoSharing API...", end='', flush=True)
r = gosharing.get_vehicles(bxl_lat, bxl_lng, radius=1000000)
if r != None:
    vehicles_count = len(r)
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles close to Brussels." % vehicles_count)

# test the nextbike api
print("Testing the NextBike API...", end='', flush=True)
r = nextbike.get_vehicles()
if r != None:
    vehicles_count = len(r['bikes'])
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles." % vehicles_count)

# test the poppy api
print("Testing the Poppy API...", end='', flush=True)
r = poppy.get_vehicles()
if r != None:
    vehicles_count = len(r)
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles." % vehicles_count)

# test the superpedestrian api
print("Testing the Superpedestrian API...", end='', flush=True)
r = superpedestrian.get_vehicles(bdx_lat, bdx_lng)
if r != None:
    vehicles_count = len(r['vehicles'])
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles close to Bordeaux." % vehicles_count)

# test the villo api
print("Testing the Villo API...", end='', flush=True)
r = villo.get_vehicles('bruxelles')
if r != None:
    vehicles_count = 0 
    for z in r:
        vehicles_count += z['totalStands']['availabilities']['bikes']
    if vehicles_count <= 0:
        print("Offline.")
    else:
        print("Online: %i vehicles close to Brussels." % vehicles_count)
