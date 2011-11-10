import time
import threading

import xbmcaddon
import xbmcgui

from temperature import Temperature

import vera.device

import gui.controlid as controlid
import controlid.dimmable_light
import controlid.hvac

# See xbmc/guilib/Key.h in XMBC sources
ACTION_MOVE_LEFT        =  1
ACTION_MOVE_RIGHT       =  2
ACTION_MOVE_UP          =  3
ACTION_MOVE_DOWN        =  4
ACTION_ENTER            =  7
ACTION_PREVIOUS_MENU    = 10 

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class DimLightThread( threading.Thread ):

    def __init__(self, gui_):
        threading.Thread.__init__(self)
        self.gui = gui_
        self.device = gui_.device
        self.vera = gui_.parent.vera

    def run(self):
        self.runThread = True
        slider = self.gui.getControl(controlid.dimmable_light.SLIDER)
        while(self.runThread):
            newValue = slider.getPercent()
            if newValue != int( float( self.device['level'] ) ):  
                vera.device.dim(self.device, self.vera, newValue)
            time.sleep(1)

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.dimmerThread = DimLightThread(self)

    def onInit(self):
        self.slider().setPercent( int( float( self.device['level'] ) ) )
        self.dimmerThread.start()

    def slider(self):
        return self.getControl(controlid.dimmable_light.SLIDER)

    def onAction(self, action):
        if action in (ACTION_PREVIOUS_MENU, ACTION_ENTER):
            self.dimmerThread.runThread = False
            self.close()
        elif action == ACTION_MOVE_UP:
            self.slider().setPercent(100)
        elif action == ACTION_MOVE_DOWN:
            self.slider().setPercent(0)

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
                    self.heat.k -= 0.4
                elif action == ACTION_MOVE_RIGHT:
                    self.heat.k += 0.4
            elif focusedControl == self.slider_cool():
                if action == ACTION_MOVE_LEFT:
                    self.cool.k -= 0.4
                elif action == ACTION_MOVE_RIGHT:
                    self.cool.k += 0.4
            self.update()

    def update(self):
        T_MIN = 273.15 # 0 C
        T_MAX = 313.15 # 40 C

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

