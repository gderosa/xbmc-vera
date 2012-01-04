import  socket

import  xbmcaddon
import  xbmcgui

from    gui.xbmc    import *

import  gui.popup

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class Camera( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.vera   = self.parent.vera

    def onInit(self):
        pass

    def onAction(self, action):
        if      action == ACTION_PREVIOUS_MENU:
            self.close()
        elif    action == ACTION_ENTER:
            self.close()


# Compat
gui.popup.Camera = Camera
