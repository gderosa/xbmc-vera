import xbmc
import xbmcgui
import xbmcaddon

import controlid 

__addon__ = xbmcaddon.Addon()
__cwd__ = __addon__.getAddonInfo('path')

class GUI( xbmcgui.WindowXML ):
    def __init__( self, *args, **kwargs ):
        pass

    def onInit( self ):
        pass

    def onClick(self, controlID):
        # if controlID == 2001:
        if controlID == controlid.SETTINGS:
            self.settingsOpen = True
            __addon__.openSettings()
