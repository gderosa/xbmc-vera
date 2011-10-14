import xbmc
import xbmcgui
import xbmcaddon

import vera
import controlid 

__addon__   = xbmcaddon.Addon()
__cwd__     = __addon__.getAddonInfo('path')

class GUI( xbmcgui.WindowXML ):
    def __init__(self, *args, **kwargs):
        self.buttonIDToRoom = {}

    def onInit(self):
        self.updateVera()
        self.hideRooms()

    def onClick(self, controlID):
        if      controlID == controlid.SETTINGS:
            __addon__.openSettings()
            self.updateVera()
        elif    controlID == controlid.GET_DATA:
            self.vera.getData()
            self.updateRooms()
        elif    controlID == controlid.EXIT:
            self.close()
        elif    controlID in self.buttonIDToRoom.keys():
            room = self.buttonIDToRoom[controlID]
            roomUI = xbmcgui.WindowXML('room.xml', __cwd__, 'Default')
            roomUI.getControl(10101).setLabel(room['name'])
            roomUI.doModal()
            del roomUI


    def updateRooms(self):
        rooms = self.vera.data['rooms']
        
        self.showLabel(controlid.ROOM_NONE, '(other devices and scenes)')

        controlID = controlid.ROOM_FIRST
        for room in rooms:
            self.showLabel(controlID, room['name'])
            self.buttonIDToRoom[controlID] = room
            controlID += 1

        self.hideRooms(controlID)

    def showLabel(self, controlID, label):
        control = self.getControl(controlID)
        control.setVisible(True)
        control.setLabel(label)

    def hideRooms(self, first=controlid.ROOM_FIRST):
        for controlID in range(first, controlid.ROOM_LAST + 1):
            button = self.getControl(controlID)
            button.setVisible(False)

    def updateVera(self):
        self.vera = vera.Controller(__addon__.getSetting('controller_ip'))
