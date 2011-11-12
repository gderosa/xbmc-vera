import sys
import re
import time
import threading
import socket
import httplib

import xbmc
import xbmcgui
import xbmcaddon

import vera
import vera.device 
import vera.device.category

import gui.controlid.main as controlid
import gui.device

from gui.xbmc import * 

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class UpdateThread(threading.Thread):

    def __init__(self, gui_):
        threading.Thread.__init__(self)
        self.gui = gui_
        self.lastErrorMsg = ''

    def run(self):
        while(self.gui.runUpdateThread):
            try:
                self.gui.vera.update()
                self.gui.update()
            except socket.error as e:
                msg = 'socket: %s' % e.__str__() 
                if msg != self.lastErrorMsg:
                    error_dialog = xbmcgui.Dialog()
                    error_dialog.ok( 'Error', msg )
                self.lastErrorMsg = msg
                if self.gui.runUpdateThread:
                    time.sleep(1)
            except httplib.BadStatusLine:
                if self.gui.runUpdateThread:
                    raise
                else: # socket has been deliberately shutdown
                    pass

class GUI( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.buttonIDToRoom = {}
        self.buttonIDToDevice = {}
        self.setVera()
        self.currentRoom = None
        self.setUpdateThread()

    def onInit(self):
        self.hideRooms()
        self.hideRoomDevices()
        self.startUpdateThread()

    def setUpdateThread(self):
        self.runUpdateThread = True
        self.updateThread = UpdateThread(self)

    def startUpdateThread(self):
        if not self.updateThread:
            self.setUpdateThread()
        self.updateThread.start()
    
    def killUpdateThread(self):
        self.runUpdateThread = False
        
        try:
            # Yeah, this is necessary to 'kill' the awaiting http client
            if self.vera.updateConnection.sock:
                self.vera.updateConnection.sock.shutdown(socket.SHUT_RDWR)
        except AttributeError:
            pass

        self.updateThread.join()
        self.updateThread = None

    def exit(self):
        self.killUpdateThread()
        self.close()

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.exit()

    def onClick(self, controlID):
        # Top buttons
        if      controlID == controlid.SETTINGS:
            __addon__.openSettings()
            self.killUpdateThread()
            self.setVera()
            self.startUpdateThread()
        elif    controlID == controlid.GET_DATA:
            self.vera.getData()
            self.updateRooms()
        elif    controlID == controlid.EXIT:
            self.exit()

        # Rooms
        elif    controlID in self.buttonIDToRoom.keys():
            room_ = self.buttonIDToRoom[controlID]
            self.fillRoom(room_)
        elif    controlID == controlid.ROOM_NONE:
            self.fillRoom(None) 

        # Devices
        elif    controlID in self.buttonIDToDevice.keys():
            device = self.buttonIDToDevice[controlID]
            if gui.device.simplySwitchable(device):
                vera.device.toggle(device, vera_controller=self.vera) 
            else: # requires a new window
                gui.device.popup(self, device)

    def update(self):
        self.updateRooms()
        self.fillRoom(self.currentRoom)

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
        self.hideControls(first, controlid.ROOM_LAST) 

    def hideRoomDevices(self, \
            first=controlid.room.DEVICE_FIRST_GROUP, 
            last=controlid.room.DEVICE_LAST_GROUP   ): 
        self.hideControls(first,last)

    def hideControls(self, firstID, lastID):
        for controlID in range(firstID, lastID + 1):
            control = self.getControl(controlID)
            control.setVisible(False)

    def setVera(self):
        self.vera = vera.Controller(__addon__.getSetting('controller_address'))

    def fillRoom(self, room):
        self.currentRoom = room

        devices = self.vera.data['devices']
        buttonID = controlid.room.DEVICE_FIRST_BUTTON
        for device in devices:
            if device['category'] in vera.device.category.DISPLAYABLE:
                if \
                        ( room and int(device['room']) == int(room['id']) ) or \
                        ( not room and not int(device['room']) )            :
                    self.showDeviceButton(buttonID, device)
                    self.buttonIDToDevice[buttonID] = device
                    buttonID += 1

        groupID = controlid.room.buttonToGroup(buttonID) 
        self.hideRoomDevices(groupID)
        

    def showDeviceButton(self, buttonID, device):
        button = self.getControl(buttonID)
        button.setLabel(device['name'])

        self.setDeviceButtonIcon(     buttonID, device    )
        self.setDeviceButtonComment(  buttonID, device    )
        self.setDeviceStateColor(     buttonID, device    )
        self.setDeviceInfo(           buttonID, device    )

        self.showDeviceButtonIconGroup(buttonID)

    def setDeviceButtonIcon(self, buttonID, device):
        iconID = controlid.room.buttonToIcon(buttonID)
        icon = self.getControl(iconID)
        image = gui.device.icon(device)
        icon.setImage(image)

    def setDeviceButtonComment(self, buttonID, device):
        labelID = controlid.room.buttonToComment(buttonID)
        label = self.getControl(labelID)
        if 'comment' in device.keys():
            # turn '_Light: My message' into 'My message'
            # with or w/o leading underscore
            text = re.sub(                          \
                    '^_?' + device['name'] + ': ',  \
                    '',                             \
                    device['comment']               \
            )
            textWithTags = '[I][COLOR grey]%s[/COLOR][/I]' % text
            label.setLabel(textWithTags)
        else:
            label.setLabel('')

    def setDeviceStateColor(self, buttonID, device):
        stateBgID = controlid.room.buttonToStateBg(buttonID)
        bgImage = self.getControl(stateBgID)
        bgImageFile = gui.device.stateBgImage(device)
        bgImage.setImage(bgImageFile)

    def setDeviceInfo(self, buttonID, device):
        labelID = controlid.room.buttonToInfo(buttonID)
        label = self.getControl(labelID)
        string = gui.device.essentialInfo(
                device,
                temperature_unit=self.vera.data['temperature']
        )
        label.setLabel(string)

    def showDeviceButtonIconGroup(self, buttonID):
        groupID = controlid.room.buttonToGroup(buttonID)
        group = self.getControl(groupID)
        group.setVisible(True)


