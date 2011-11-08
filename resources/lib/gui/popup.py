import xbmcaddon
import xbmcgui

# keymap.xml ?
ACTION_PREVIOUS_MENU = 10

__addon__   = xbmcaddon.Addon()
__cwd__     = __addon__.getAddonInfo('path')

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        pass

    def onInit(self):
        pass


