# This shall be replaced by i18n stuff

MODES = {
    'Off':              'Off',
    'AutoChangeOver':   'Auto',
    'HeatOn':           'Heat',
    'CoolOn':           'Cool'
}

FAN_MODES = {
    'Auto':             'Auto',
    'ContinuousOn':     'Always On'
}

def button_fan(mode):
    return FAN_MODES[mode]

def button_mode(mode):
    return MODES[mode]


