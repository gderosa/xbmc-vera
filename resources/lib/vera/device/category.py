# http://wiki.mios.com/index.php/Luup_Device_Categories
# http://wiki.micasaverde.com/index.php/UI_Simple#Status_of_the_device_or_scene_and_control_buttons

INTERFACE           =  1
DIMMABLE_LIGHT      =  2
SWITCH              =  3
SECURITY_SENSOR     =  4
THERMOSTAT          =  5
CAMERA              =  6
DOOR_LOCK           =  7
WINDOW_COVERING     =  8
REMOTE_CONTROL      =  9
IR_TRANSMITTER      = 10
HUMIDITY_SENSOR     = 16
TEMPERATURE_SENSOR  = 17
LIGHT_SENSOR        = 18
POWER_METER         = 21

MOTION_SENSOR = SECURITY_SENSOR # alias

DISPLAYABLE = [
        DIMMABLE_LIGHT, SWITCH, SECURITY_SENSOR, THERMOSTAT, CAMERA, DOOR_LOCK,
        WINDOW_COVERING, HUMIDITY_SENSOR, TEMPERATURE_SENSOR, LIGHT_SENSOR,
        POWER_METER ]


