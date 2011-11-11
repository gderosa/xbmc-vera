# http://wiki.micasaverde.com/index.php/Luup_Variables
# http://wiki.micasaverde.com/index.php/UI_Simple#Status_of_the_device_or_scene_and_control_buttons

import xbmcaddon

from vera.device.category   import *
from vera.device.state      import *

import gui.popup.all_categories

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

CATEGORY_ICONS = {
        DIMMABLE_LIGHT:     'devices/Dimmable_Light.png',
        BINARY_LIGHT:       'devices/Binary_Light.png',         # or SWITCH
        MOTION_SENSOR:      'devices/Motion_Sensor.png',
        THERMOSTAT:         'devices/Thermostat.png',
        CAMERA:             'devices/Ip_Camera.png',
        DOOR_LOCK:          'devices/Door_Lock.png',
        WINDOW_COVERING:    'devices/Window_Covering.png',
        HUMIDITY_SENSOR:    'devices/Humidity_Sensor.png',
        TEMPERATURE_SENSOR: 'devices/Temperature_Sensor.png',
        LIGHT_SENSOR:       'devices/Light_Sensor.png',
        POWER_METER:        'devices/Power_Meter.png',
        GENERIC:            'devices/device.png'
}

# NOTE: dictionary keys are tuples!
STATE_BACKGROUNDS = {
        NONE:               'devices/state_grey.png',
        PENDING:            'devices/state_blue.png',
        ERROR:              'devices/state_red.png',
        SUCCESS:            'devices/state_green.png'
}

# no "write" action from gui other than "toggle" (on/off, arm/disarm etc.) 
SIMPLY_SWITCHABLE = [ BINARY_LIGHT, MOTION_SENSOR, DOOR_LOCK  ]

def simplySwitchable(device):
    return (device['category'] in SIMPLY_SWITCHABLE) 

def icon(device):
    category = device['category']
    if      category == DIMMABLE_LIGHT:
        try:
            level = float(device['level'])
        except KeyError:
            level = 0.0
        level_round = round(level/25)*25 # 0.0, 25.0, 50.0, 75.0 or 100.0 
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
    elif    category == DOOR_LOCK: 
        if int(device['status']):
            return 'devices/Door_Lock_100.png'
        else:
            return 'devices/Door_Lock_0.png'
    else: # icon does not depend upon status
        try:
            return CATEGORY_ICONS[ category ] 
        except KeyError:
            return CATEGORY_ICONS[ GENERIC ]

def stateBgImage(device):
    if 'state' in device.keys():
        for type_ in (NONE, PENDING, ERROR, SUCCESS):
            # on updates you may get strings instead of integers :-(
            if int(device['state']) in type_: 
                return STATE_BACKGROUNDS[ type_ ]  
        raise RuntimeError, \
                'invalid device[\'state\'] ' + \
                device['state'] + ' (' + str(type(device['state'])) + ')' 
    else:
        return STATE_BACKGROUNDS[ NONE ]  

def essentialInfo(device, temperature_unit=''):
    if device['category'] == DIMMABLE_LIGHT:
        if 'watts' in device.keys():
            return '%sW' % device['watts']
        elif 'level' in device.keys():
            return '%s%%' % device['level']
        else:
            return '0%'
    if device['category'] in (BINARY_LIGHT, POWER_METER):
        if 'watts' in device.keys():
            return '%sW' % device['watts']
    if device['category'] == MOTION_SENSOR:
        if 'armed' in device.keys():
            if device['armed'] == '1':
                return 'Armed'
            if device['armed'] == '0':
                return 'Bypass'
    if device['category'] == THERMOSTAT:
        mode, heat, cool = device['mode'], device['heatsp'], device['coolsp']
        values = mode, heat, cool, temperature_unit
        if      mode == 'Off':
            return u'Mode: %s  [COLOR grey]Heat: %s  Cool: %s  (\xb0%s)[/COLOR]' % values
        elif    'Heat' in mode:
            return u'Mode: %s  Heat: %s  [COLOR grey]Cool: %s[/COLOR]  (\xb0%s)' % values
        elif    'Cool' in mode:
            return u'Mode: %s  [COLOR grey]Heat: %s[/COLOR]  Cool: %s  (\xb0%s)' % values
        else:
            return u'Mode: %s  Heat: %s  Cool: %s  (\xb0%s)'                     % values
    if device['category'] == DOOR_LOCK:
        if 'locked' in device.keys():
            if int(device['locked']):
                return 'Locked'
            else:
                return 'Unlocked'
    if device['category'] == WINDOW_COVERING:
        return 'Level: %s' % device['level'] 
    if device['category'] == HUMIDITY_SENSOR:
        return '%s%%' % device['humidity']       
    if device['category'] == TEMPERATURE_SENSOR:
        return u'%s\xb0%s' % (device['temperature'], temperature_unit) # degree sign
    if device['category'] == LIGHT_SENSOR:
        return 'Level: %s' % device['light']
    return ''

def popup(parent_, device_):
    popup = None

    if device_['category'] in ( DIMMABLE_LIGHT, WINDOW_COVERING ):
        popup = gui.popup.DimmableLight(                    \
                'dimmable-light.xml', __cwd__, 'Default',   \
                parent=parent_, device = device_            )  
        popup.doModal()

    elif device_['category'] == HVAC:
        popup = gui.popup.HVAC(                             \
                'hvac.xml', __cwd__, 'Default',             \
                parent=parent_, device = device_            )
        popup.doModal()
    
    del popup # isn't this automatically garbaged?





