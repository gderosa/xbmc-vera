import time
import threading

import xbmcaddon
import xbmcgui

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

    def run(self):
        while(True):
            print('DimLightThread run')
            time.sleep(1)

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.dimmerThread = DimLightThread(self)

    def onInit(self):
        slider = self.getControl(controlid.dimmable_light.SLIDER)
        slider.setPercent(int(self.device['level'])) 

        self.dimmerThread.start()


