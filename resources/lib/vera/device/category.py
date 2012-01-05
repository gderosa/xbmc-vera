# See also:
# http://wiki.mios.com/index.php/Luup_Device_Categories
# http://wiki.micasaverde.com/index.php/UI_Simple#Status_of_the_device_or_scene_and_control_buttons

GENERIC             =  0

INTERFACE           =  1
DIMMABLE_LIGHT      =  2
BINARY_LIGHT        =  3
MOTION_SENSOR       =  4
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

# aliases
SECURITY_SENSOR = MOTION_SENSOR 
SWITCH          = BINARY_LIGHT
BINARY_SWITCH   = BINARY_LIGHT
DIMMER          = DIMMABLE_LIGHT
HVAC            = THERMOSTAT


# CAMERA and DOOR_LOCK not implemented and hidden, right now
DISPLAYABLE = [
        DIMMABLE_LIGHT, BINARY_LIGHT, MOTION_SENSOR, THERMOSTAT, 
        WINDOW_COVERING, HUMIDITY_SENSOR, TEMPERATURE_SENSOR, LIGHT_SENSOR,
        POWER_METER ]



