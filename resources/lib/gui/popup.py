import time
import threading

import xbmcaddon
import xbmcgui

import vera.device

import gui.controlid as controlid
import controlid.dimmable_light

# keymap.xml ?
ACTION_PREVIOUS_MENU = 10

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class DimLightThread(threading.Thread):

    def __init__(self, gui_):
        threading.Thread.__init__(self)
        self.gui = gui_
        self.device = gui_.device
        self.vera = gui_.parent.vera

    def run(self):
        slider = self.gui.getControl(controlid.dimmable_light.SLIDER)
        while(True):
            time.sleep(1)
            newValue = slider.getPercent()
            if newValue != int( float( self.device['level'] ) ):  
                vera.device.dim(self.device, self.vera, newValue)

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.dimmerThread = DimLightThread(self)

    def onInit(self):
        slider = self.getControl(controlid.dimmable_light.SLIDER)
        slider.setPercent(int(float(self.device['level'])))  

        self.dimmerThread.start()


