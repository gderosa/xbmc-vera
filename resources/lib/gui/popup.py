import xbmcaddon
import xbmcgui

import gui.controlid as controlid
import controlid.dimmable_light

# keymap.xml ?
ACTION_PREVIOUS_MENU = 10

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']

    def onInit(self):
        slider = self.getControl(controlid.dimmable_light.SLIDER)
        slider.setPercent(int(self.device['level'])) 


