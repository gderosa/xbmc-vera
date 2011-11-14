# Implements http://wiki.micasaverde.com/index.php/UI_Simple#Status_of_the_device_or_scene_and_control_buttons

from vera.device import category 

HVAC_MODES      = ['Off', 'AutoChangeOver', 'HeatOn', 'CoolOn'] 
HVAC_FAN_MODES  = ['Auto', 'ContinuousOn']

# turn on/off a BinaryLight, arm/bypass a motion sensor etc.
def toggle(device, vera_controller):
    
    if device['category'] == category.BINARY_LIGHT:
        newTargetValue = '1'
        if int(device['status']):
            newTargetValue = '0'
        vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget'           + \
'&newTargetValue=' + newTargetValue                                         
        )

    elif device['category'] == category.MOTION_SENSOR:
        Value = '1'
        if int(device['armed']):
            Value = '0'
        vera_controller.GET( \
'/data_request?id=variableset&DeviceNum=' + str(device['id'])               + \
'&serviceId=urn:micasaverde-com:serviceId:SecuritySensor1&Variable=Armed'   + \
'&Value=' + Value                                                            
        )

    elif device['category'] == category.DOOR_LOCK:
        pass # TODO


def dim(device, vera_controller, level):
    if device['category'] in \
            ( category.DIMMABLE_LIGHT, category.WINDOW_COVERING ):
        vera_controller.GET(
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget'      + \
'&newLoadlevelTarget=' + str(level)
        )

def hvac_set_mode(device, vera_controller, mode):
    if device['category'] == category.HVAC:
        vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:HVAC_UserOperatingMode1'                 + \
'&action=SetModeTarget&NewModeTarget=' + mode
        )
def hvac_set_fan(device, vera_controller, mode):
    if device['category'] == category.HVAC:
        vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:HVAC_FanOperatingMode1'                  + \
'&action=SetMode&NewMode=' + mode
        )

def hvac_set_points(device, vera_controller, heat=None, cool=None):
    if device['category'] == category.HVAC:
        if heat != None:
            vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Heat'               + \
'&action=SetCurrentSetpoint&NewCurrentSetpoint=' + str(heat)
            )
        if cool != None:
            vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:TemperatureSetpoint1_Cool'               + \
'&action=SetCurrentSetpoint&NewCurrentSetpoint=' + str(cool)
            )


