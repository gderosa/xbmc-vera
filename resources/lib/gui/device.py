from vera.device.category   import *
from vera.device.state      import *

CATEGORY_ICONS = {
        DIMMABLE_LIGHT:     'devices/Dimmable_Light.png',
        SWITCH:             'devices/Binary_Light.png',
        MOTION_SENSOR:      'devices/Motion_Sensor.png',
        THERMOSTAT:         'devices/Thermostat.png',
        CAMERA:             'devices/Ip_Camera.png',
        DOOR_LOCK:          'devices/Door_Lock.png',
        WINDOW_COVERING:    'devices/Window_Covering.png',
        HUMIDITY_SENSOR:    'devices/Humidity_Sensor.png',
        TEMPERATURE_SENSOR: 'devices/Temperature_Sensor.png',
        LIGHT_SENSOR:       'devices/Light_Sensor.png',
        POWER_METER:        'devices/Power_Meter.png'
}

def icon(device):
    category = device['category']
    if      category == DIMMABLE_LIGHT:
        level = float(device['level'])
        level_round = round(level/25)*25 # 0, 25, 50, 75 or 100 
        return 'devices/Dimmable_Light_%d.png' % level_round
    elif    category == SWITCH:
        if int(device['status']):
            return 'devices/Binary_Light_100.png'
        else:
            return 'devices/Binary_Light_0.png'
    elif    category == MOTION_SENSOR:
        if int(device['tripped']):
            return 'devices/Motion_Sensor_100.png'
        else:
            return 'devices/Motion_Sensor_0.png'
    elif    category == DOOR_LOCK: # TODO
        return 'devices/Door_Lock.png'
    else: # icon does not depend upon status
        return CATEGORY_ICONS[category] 

def stateBgImage(device):
    if 'state' in device.keys():
        state = device['state']
        if      state in NONE:
            return 'devices/state_grey.png'
        elif    state in PENDING:
            return 'devices/state_blue.png'
        elif    state in ERROR:
            return 'devices/state_red.png'
        elif    state in SUCCES:
            return 'devices/state_green.png'
    else:
        return 'devices/state_grey.png'


