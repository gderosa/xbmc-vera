import  socket

import  xbmc
import  xbmcaddon
import  xbmcgui

from    util.temperature            import Temperature
from    util.cycle                  import Cycle
import  vera.device
from    gui.xbmc                    import *
from    gui                         import controlid, message
import  gui.controlid.hvac, gui.message.hvac

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
        xbmc.enableNavSounds(True)

        try:
            focusedControl = self.getFocus()
        except TypeError:
            return

        if      action == ACTION_PREVIOUS_MENU:
            self.close()
        elif    action == ACTION_ENTER:
            self.commit()
            self.close()
        else:
            if focusedControl == self.slider_heat():
                if action in (ACTION_MOUSE_CLICK + ACTION_MOUSE_WHEEL) or \
                        action == ACTION_MOUSE_DRAG: 
                    percent_heat = self.slider_heat().getPercent()
                    self.heat.k = \
                            T_MIN + percent_heat*( ( T_MAX - T_MIN ) / 100.0 )
                    self.update_heat(slider=False)
                elif action == ACTION_MOVE_LEFT:
                    self.heat.k -= T_STEP
                    self.update_heat()
                    xbmc.enableNavSounds(False)
                elif action == ACTION_MOVE_RIGHT:
                    self.heat.k += T_STEP
                    self.update_heat()
                    xbmc.enableNavSounds(False)
            elif focusedControl == self.slider_cool():
                if action in (ACTION_MOUSE_CLICK + ACTION_MOUSE_WHEEL) or \
                        action == ACTION_MOUSE_DRAG:
                    percent_cool = self.slider_cool().getPercent()
                    self.cool.k = \
                            T_MIN + percent_cool*( ( T_MAX - T_MIN ) / 100.0 )
                    self.update_cool(slider=False)
                if action == ACTION_MOVE_LEFT:
                    self.cool.k -= T_STEP
                    self.update_cool()
                elif action == ACTION_MOVE_RIGHT:
                    self.cool.k += T_STEP
                    self.update_cool()
            elif focusedControl == self.previouslyFocused == self.button_fan():
                if action in \
(ACTION_MOVE_DOWN, ACTION_MOVE_RIGHT, ACTION_MOUSE_LEFT_CLICK):
                    self.fanMode.cycle()
                    self.update_fan()
                elif action == ACTION_MOVE_LEFT:
                    self.fanMode.cycle_back()
                    self.update_fan()
            elif focusedControl == self.previouslyFocused == self.button_mode():
                if action in \
(ACTION_MOVE_UP, ACTION_MOVE_RIGHT, ACTION_MOUSE_LEFT_CLICK):
                    self.mode.cycle()
                    self.update_mode()
                elif action == ACTION_MOVE_LEFT:
                    self.mode.cycle_back()
                    self.update_mode()

        self.previouslyFocused = focusedControl

    def update(self):
        self.update_heat()
        self.update_cool()
        self.update_mode()
        self.update_fan()

    def update_heat(self, slider=True):
        if slider:
            if      self.heat.k < T_MIN:
                self.slider_heat().setPercent(0)
            elif    self.heat.k > T_MAX:
                self.slider_heat().setPercent(100)
            else:
                percent = int ( round( \
                        ( (self.heat.k - T_MIN) / (T_MAX - T_MIN) ) * 100 \
                ) )
                self.slider_heat().setPercent(percent)

        self.label_heat().setLabel( \
                u'%.1f \xb0%s' % (self.heat.value, self.heat.unit) ) 

    def update_cool(self, slider=True):
        if slider:
            if      self.cool.k < T_MIN:
                self.slider_cool().setPercent(0)
            elif    self.cool.k > T_MAX:
                self.slider_cool().setPercent(100)
            else:
                percent = int ( round( \
                        ( (self.cool.k - T_MIN) / (T_MAX - T_MIN) ) * 100 \
                ) )
                self.slider_cool().setPercent(percent)

        self.label_cool().setLabel( \
                u'%.1f \xb0%s' % (self.cool.value, self.cool.unit) ) 

    def update_mode(self):
        _msg = message.hvac.button_mode( self.mode.current )
        self.button_mode().setLabel( _msg.upper() )  

    def update_fan(self):
        _msg = message.hvac.button_fan( self.fanMode.current )
        self.button_fan().setLabel( _msg.upper() )   

    def commit(self):
        try:
            vera.device.hvac_set_mode( \
                    self.device, self.vera, self.mode.current )
            vera.device.hvac_set_fan( \
                    self.device, self.vera, self.fanMode.current )

            heatsp = self.heat.value
            coolsp = self.cool.value
            vera.device.hvac_set_points( \
                    self.device, self.vera, heat=heatsp, cool=coolsp )
        except socket.error as e:
            msg = 'socket: %s' % e.__str__()
            error_dialog = xbmcgui.Dialog()
            error_dialog.ok( 'Network Connection Error', msg )



# Compat
gui.popup.HVAC = HVAC

