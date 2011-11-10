# Implements http://wiki.micasaverde.com/index.php/UI_Simple#Status_of_the_device_or_scene_and_control_buttons

from vera.device import category 

HVAC_FAN_MODES = ['Auto', 'ContinuousOn']

# turn on/off a BinaryLight, arm/bypass a motion sensor etc.
def toggle(device, vera_controller):
    
    if device['category'] == category.BINARY_LIGHT:
        newTargetValue = '1'
        if int(device['status']):
            newTargetValue = '0'
        vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget'           + \
'&newTargetValue=' + newTargetValue                                           \
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
    if device['category'] == category.DIMMABLE_LIGHT:
        vera_controller.GET( \
'/data_request?id=action&DeviceNum=' + str(device['id'])                    + \
'&serviceId=urn:upnp-org:serviceId:Dimming1&action=SetLoadLevelTarget'      + \
'&newLoadlevelTarget=' + str(level)                                           \
        )

