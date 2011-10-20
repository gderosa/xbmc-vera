import re

import xbmc
import xbmcgui
import xbmcaddon

import vera.device.category

import gui.controlid.room as controlid
import gui.device

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
                    self.showButton(buttonID, device)
                    buttonID += 1

    def showButton(self, buttonID, device):
        button = self.getControl(buttonID)
        button.setLabel(device['name'])

        self.setButtonIcon(     buttonID, device    ) 
        self.setButtonComment(  buttonID, device    )
        self.setStateColor(     buttonID, device    ) 
        self.setInfo(           buttonID, device    )

        self.showButtonIconGroup(buttonID) 

    def setButtonIcon(self, buttonID, device):
        iconID = controlid.buttonToIcon(buttonID)
        icon = self.getControl(iconID)
        image = gui.device.icon(device)
        icon.setImage(image) 

    def setButtonComment(self, buttonID, device):
        if 'comment' in device.keys(): 
            
            labelID = controlid.buttonToComment(buttonID)
            label = self.getControl(labelID)

            # turn '_Light: My message' into 'My message'
            # with or w/o leading underscore
            text = re.sub(                          \
                    '^_?' + device['name'] + ': ',  \
                    '',                             \
                    device['comment']               \
            )
            textWithTags = '[I][COLOR grey]%s[/COLOR][/I]' % text
            label.setLabel(textWithTags)

    def setStateColor(self, buttonID, device):
        stateBgID = controlid.buttonToStateBg(buttonID) 
        bgImage = self.getControl(stateBgID) 
        bgImageFile = gui.device.stateBgImage(device)
        bgImage.setImage(bgImageFile) 

    def setInfo(self, buttonID, device):
        labelID = controlid.buttonToInfo(buttonID)
        label = self.getControl(labelID)
        string = gui.device.essentialInfo(
                device, 
                temperature_unit=self.vera.data['temperature']
        )
        label.setLabel(string)

    def showButtonIconGroup(self, buttonID):
        groupID = controlid.buttonToGroup(buttonID) 
        group = self.getControl(groupID)
        group.setVisible(True)

    def hideDevices(self, first=controlid.DEVICE_FIRST_GROUP):
        for groupID in range(first, controlid.DEVICE_LAST_GROUP + 1):
            group = self.getControl(groupID)
            group.setVisible(False)




