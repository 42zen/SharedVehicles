import os

WIN_NUL_REDIR = ">nul 2>nul"
NUL_REDIR = WIN_NUL_REDIR

WIN_ERR_REDIR = "2>&1"
ERR_REDIR = WIN_ERR_REDIR

ADB_BIN_PATH = 'C:/Programs/AndroidDebugBridge/adb.exe'

server_is_running = False

def start_server():
    os.system(f'{ADB_BIN_PATH} start-server {NUL_REDIR}')
    server_is_running = True
    return True

def kill_server():
    os.system(f'{ADB_BIN_PATH} kill-server {NUL_REDIR}')
    server_is_running = False
    return True

def shell(command, serial=None, return_process=False):
    if server_is_running == False:
        start_server()
    adb_command_prefix = f'{ADB_BIN_PATH} ' + (('-s %s ' % serial) if serial != None else '') + 'shell '
    cmd = adb_command_prefix + command + ' ' + ERR_REDIR
    process = os.popen(cmd)
    if return_process == True:
        return process
    result = process.read()
    process.close()
    return result

def is_connected():
    if server_is_running == False:
        start_server()
    if shell('echo alive')[:5] == 'alive':
        return True
    return False

def get_positions(type='network'):
    process = shell(f'dumpsys location', return_process=True)
    line = process.readline()
    if line.find('no devices/emulators found') != -1:
        return None
    while line != '':
        if line.find('last location') != -1:
            if line.find(type) != -1:
                break
        line = process.readline()
    process.close()
    if line != '':
        line = line[line.find(type) + len(type) + 1:]
        line = line[:line.find(' ')]
        pos = line.find(',')
        line = line[:pos] + '.' + line[pos + 1:]
        pos = line.find(',')
        lat = float(line[:pos])
        lng = line[pos + 1:]
        pos = lng.find(',')
        lng = float(lng[:pos] + '.' + lng[pos + 1:])
        positions = {'lat':lat, 'lng':lng}
        return positions
    return None
