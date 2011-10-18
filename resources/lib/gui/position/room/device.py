# gui.position.room.device module

# must match skin...

import gui.size.room.device

from gui.spacing.room.device import ICON_MARGIN_RIGHT
from gui.step.room.device import Y as DELTA_Y
from gui.controlid.room import DEVICE_FIRST as FIRST_CONTROL_ID


FIRST_CORNER = 100, 200

BUTTON_WIDTH, BUTTON_HEIGHT = gui.size.room.device.BUTTON
ICON_SIZE = gui.size.room.device.ICON[0] 


FIRST_CORNER_X, FIRST_CORNER_Y = FIRST_CORNER
FIRST_ICON_X = FIRST_CORNER_X + BUTTON_WIDTH - ICON_MARGIN_RIGHT - ICON_SIZE
FIRST_ICON_Y = FIRST_CORNER_Y + (BUTTON_HEIGHT - ICON_SIZE)/2 

def icon(controlID):
    x = FIRST_ICON_X
    y = FIRST_ICON_Y + (controlID - FIRST_CONTROL_ID) * DELTA_Y
    return x, y


