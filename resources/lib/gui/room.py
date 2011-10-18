import xbmc
import xbmcgui
import xbmcaddon

import vera.device.category

import gui.controlid.room as controlid

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
        if controlID == controlid.EXIT:
            self.close()

    def updateDevices(self):
        devices = self.vera.data['devices']

        buttonID = controlid.DEVICE_FIRST_BUTTON
        for device in devices:
            if device['category'] in vera.device.category.DISPLAYABLE:
                if \
                        ( self.room and device['room'] == self.room['id'] ) or \
                        ( not self.room and device['room'] == 0 ) :
                    self.showButton(buttonID, device['name'])
                    buttonID += 1

    def showButton(self, buttonID, label):
        button = self.getControl(buttonID)
        button.setLabel(label)
        self.showButtonIconGroup(buttonID) 

    def showButtonIconGroup(self, buttonID):
        groupID = controlid.buttonToGroup(buttonID) 
        group = self.getControl(groupID)
        group.setVisible(True)

    def hideDevices(self, first=controlid.DEVICE_FIRST_GROUP):
        for groupID in range(first, controlid.DEVICE_LAST_GROUP + 1):
            group = self.getControl(groupID)
            group.setVisible(False)




