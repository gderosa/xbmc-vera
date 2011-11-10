import  xbmcaddon
import  xbmcgui

from    util.temperature            import Temperature
import  vera.device
from    gui.xbmc                    import *
from    gui                         import controlid

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

T_MIN = 273.15 # 0 C
T_MAX = 313.15 # 40 C

T_STEP = ( T_MAX - T_MIN ) / 100.0

class HVAC( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.vera   = self.parent.vera
        self.heat = Temperature()
        self.cool = Temperature()
        self.heat.c = 20
        self.cool.c = 18
        self.temperatureUnit = 'C'

    def onInit(self):
        self.update()

    def slider_heat(self):
        return self.getControl(controlid.hvac.SLIDER_HEAT)
    def slider_cool(self):
        return self.getControl(controlid.hvac.SLIDER_COOL)
    
    def label_heat(self):
        return self.getControl(controlid.hvac.LABEL_HEAT)
    def label_cool(self):
        return self.getControl(controlid.hvac.LABEL_COOL)

    def onAction(self, action):
        focusedControl = self.getFocus()
        if action in (ACTION_PREVIOUS_MENU, ACTION_ENTER):
            self.close()
        else:
            if focusedControl == self.slider_heat():
                if action == ACTION_MOVE_LEFT:
                    self.heat.k -= T_STEP
                elif action == ACTION_MOVE_RIGHT:
                    self.heat.k += T_STEP
            elif focusedControl == self.slider_cool():
                if action == ACTION_MOVE_LEFT:
                    self.cool.k -= T_STEP
                elif action == ACTION_MOVE_RIGHT:
                    self.cool.k += T_STEP
            self.update()

    def update(self):
        if      self.heat.k < T_MIN:
            self.slider_heat().setPercent(0)
        elif    self.heat.k > T_MAX:
            self.slider_heat().setPercent(100)
        else:
            percent = int ( round( \
                    ( (self.heat.k - T_MIN) / (T_MAX - T_MIN) ) * 100 \
            ) )
            self.slider_heat().setPercent(percent)
        self.label_heat().setLabel(u'%.1f \xb0C' % self.heat.c) 

        if      self.cool.k < T_MIN:
            self.slider_cool().setPercent(0)
        elif    self.cool.k > T_MAX:
            self.slider_cool().setPercent(100)
        else:
            percent = int ( round( \
                    ( (self.cool.k - T_MIN) / (T_MAX - T_MIN) ) * 100 \
            ) )
            self.slider_cool().setPercent(percent)
        self.label_cool().setLabel(u'%.1f \xb0C' % self.cool.c) 

