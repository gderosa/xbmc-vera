import xbmc
import xbmcgui
import xbmcaddon

import vera.device.category

import controlid.room

class RoomUI( xbmcgui.WindowXMLDialog ):
    def __init__(self, *args, **kwargs):
        self.room = kwargs['room']
        self.vera = kwargs['vera']

    def onInit(self):
        self.hideDevices()
        label = self.getControl(10101)
        if self.room:
            label.setLabel(self.room['name'])
        else:
            label.setLabel('Devices not in any room')
        self.updateDevices()

    def onClick(self, controlID):
        if controlID == controlid.room.EXIT:
            self.close()

    def updateDevices(self):
        devices = self.vera.data['devices']

        controlID = controlid.room.DEVICE_FIRST
        for device in devices:
            if device['category'] in vera.device.category.DISPLAYABLE:
                if self.room:
                    if device['room'] == self.room['id'] :
                        self.showLabel(controlID, device['name'])
                        controlID += 1
                else:
                    if device['room'] == 0:
                        self.showLabel(controlID, device['name'])
                        controlID += 1

    def showLabel(self, controlID, label): # TODO: DRY
        control = self.getControl(controlID)
        control.setVisible(True)
        control.setLabel(label)

    def hideDevices(self, first=controlid.room.DEVICE_FIRST):
        for controlID in range(first, controlid.room.DEVICE_LAST + 1):
            button = self.getControl(controlID)
            button.setVisible(False)




