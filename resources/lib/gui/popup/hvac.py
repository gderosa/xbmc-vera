import  xbmcaddon
import  xbmcgui

from    util.temperature            import Temperature
from    util.cycle                  import Cycle
import  vera.device
from    gui.xbmc                    import *
from    gui                         import controlid, message

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

T_MIN = 273.15 # 0 C
T_MAX = 313.15 # 40 C

T_STEP = ( T_MAX - T_MIN ) / 100.0

class HVAC( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.previouslyFocused = None

        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.vera   = self.parent.vera

        self.temperatureUnit = self.vera.data['temperature'] 
        self.heat = Temperature( self.device['heatsp'], self.temperatureUnit ) 
        self.cool = Temperature( self.device['coolsp'], self.temperatureUnit )

        self.mode               = Cycle(vera.device.HVAC_MODES)
        self.mode.current       = self.device['mode']

        self.fanMode            = Cycle(vera.device.HVAC_FAN_MODES)
        try:
            self.fanMode.current    = self.device['fan']
        except KeyError:
            self.fanMode.current    = 'Auto'

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

    def button_fan(self):
        return self.getControl(controlid.hvac.FAN)
    def button_mode(self):
        return self.getControl(controlid.hvac.MODE)

    def onAction(self, action):
        focusedControl = self.getFocus()

        if      action == ACTION_PREVIOUS_MENU:
            self.close()
        elif    action == ACTION_ENTER:
            self.commit()
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
            elif focusedControl == self.previouslyFocused == self.button_fan():
                if action in (ACTION_MOVE_DOWN, ACTION_MOVE_RIGHT):
                    self.fanMode.cycle()
                elif action == ACTION_MOVE_LEFT:
                    self.fanMode.cycle_back()
            elif focusedControl == self.previouslyFocused == self.button_mode():
                if action in (ACTION_MOVE_UP, ACTION_MOVE_RIGHT):
                    self.mode.cycle()
                elif action == ACTION_MOVE_LEFT:
                    self.mode.cycle_back()                   
            self.update()

        self.previouslyFocused = focusedControl

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

        _msg = message.hvac.button_fan( self.fanMode.current )
        self.button_fan().setLabel( _msg.upper() )   
        
        _msg = message.hvac.button_mode( self.mode.current )
        self.button_mode().setLabel( _msg.upper() )  

    def commit(self):
        vera.device.hvac_set_mode(self.device, self.vera, self.mode.current)
        vera.device.hvac_set_fan(self.device, self.vera, self.fanMode.current)

