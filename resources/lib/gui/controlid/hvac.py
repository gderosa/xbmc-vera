# must reflect skin's hvac.xml !

MODE        = 105002
SLIDER_HEAT = 105003
SLIDER_COOL = 105004
FAN         = 105005

LABEL_HEAT  = 105103
LABEL_COOL  = 105104

ARROWS_MODE = 105202
ARROWS_HEAT = 105203
ARROWS_COOL = 105204
ARROWS_FAN  = 105205

def controlToArrows(controlID):
    return controlID + 200


