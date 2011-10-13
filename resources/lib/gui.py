import xbmc
import xbmcgui
import xbmcaddon

import vera

import controlid 

__addon__   = xbmcaddon.Addon()
__cwd__     = __addon__.getAddonInfo('path')

class GUI( xbmcgui.WindowXML ):
    def __init__(self, *args, **kwargs):
        pass

    def onInit(self):
        self.updateVera()

    def onClick(self, controlID):
        if      controlID == controlid.SETTINGS:
            __addon__.openSettings()
            self.updateVera()
        elif    controlID == controlid.GET_DATA:
            self.vera.getData()
            self.updateRooms()
        elif    controlID == controlid.EXIT:
            self.close()

    def updateRooms(self):
        rooms = self.vera.data['rooms']
        controlID = controlid.ROOM_FIRST
        for room in rooms:
            controlID += 1
            button = self.getControl(controlID) 
            button.setLabel(room['name'])

    def updateVera(self):
        self.vera = vera.Controller(__addon__.getSetting('controller_ip'))
