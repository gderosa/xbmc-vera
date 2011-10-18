# reflects skin's room.xml

DEVICE_FIRST_GROUP  = 33001
DEVICE_LAST_GROUP   = 33019
DEVICE_FIRST_BUTTON = 11001
DEVICE_LAST_BUTTON  = 11019

EXIT                = 19999

def buttonToGroup(buttonID):
    return buttonID + 22000
