import xbmc
import xbmcgui
import xbmcaddon

import vera

import controlid 

__addon__ = xbmcaddon.Addon()
__cwd__ = __addon__.getAddonInfo('path')

class GUI( xbmcgui.WindowXML ):
    def __init__( self, *args, **kwargs ):
        pass

    def onInit( self ):
        pass

    def onClick(self, controlID):
        if      controlID == controlid.SETTINGS:
            self.settingsOpen = True
            __addon__.openSettings()
        elif    controlID == controlid.GET_DATA:
            data = vera.getData('192.168.33.155')
            self.updateRooms(data)
        elif    controlID == controlid.EXIT:
            self.close()

    def updateRooms(self, data):
        print 'updateRooms(' + str(data) + ')'


