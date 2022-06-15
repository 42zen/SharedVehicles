# import the python libraries needed
import os
import json
import sharedmobility

# import the tools libraries needed
from tools import speech
from tools import adb


# set the settings
TARGET_FILENAME = 'vehicle.target'


def select_target(target):
    # open the target file
    target_file = open(TARGET_FILENAME, 'w')

    # save the json content in file
    json.dump(target, target_file)

    # close the tokens file
    target_file.close()

def load_target():
    # create the target variable
    target = None

    # open the target file
    target_file = None
    try:
        target_file = open(TARGET_FILENAME, 'r')
    except FileNotFoundError:
        pass

    # save, close and delete the file if needed
    if target_file != None:
        # save the target as json file
        target = json.load(target_file)

        # close the target file
        target_file.close()

        # delete the target file
        os.remove(TARGET_FILENAME)

    # return the target loaded if any
    if target != None:
        return target

    # there is no target to load
    return None

def scan():
    # check if adb is running
    if adb.is_connected() == False:
        print("Error: ADB is not connected.")
        return False

    # get GPS position from adb shell
    positions = adb.get_positions()

    # check for empty positions
    if positions == None:
        print("Error: GPS is disabled on device.")
        return False

    # get the closest vehicle
    vehicle = sharedmobility.get_closest_vehicle(positions['lat'], positions['lng'])

    # translate the brand name in french
    brand = vehicle['brand']
    if brand == 'Voi':
        brand = 'Vauille'
    elif brand == 'Lime':
        brand = 'L\'ailme'

    # build the speech text
    text = "%s, %.0f mètres." % (brand, vehicle['distance'])

    # select this target at the next shot
    select_target(vehicle)

    # prepare to ring the vehicle
    sharedmobility.prepare_ring_vehicle(vehicle)

    # run a google speech
    speech.google(text, lang='fr')

    # success
    return True

def shot():
    # get the current target if any
    vehicle = load_target()
    if vehicle == None:
        speech.google('No target.')
        return False
    
    # try to ring the target
    if sharedmobility.ring_vehicle(vehicle, prepared=True) == False:
        speech.google('Can\'t ring vehicle.')
        return False

    # success
    return True


def main():
    # TODO: get android button input
    #   How to log all inputs in the same software from 2 differents users ?
    #    1) A proxy file: adb.shell('cat /dev/input > /sdcard/input')
    #    2) Simple input reading from sdcard
    #   When input: scan() scan or shot().
    pass

scan()