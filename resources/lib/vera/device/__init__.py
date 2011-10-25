from vera.device.category import *

# turn on/off a BinaryLight, arm/disarm a motion sensor etc.
def toggle(device):
    print('vera.device.toggle(): "%s"' % device['name']) 

# True if the only action you can do is binary-switch-like
def simplySwitchable(device):
    return ( device['category'] in SIMPLY_SWITCHABLE )

