# Also used for Window Covering

import  time
import  socket
import  threading

import  xbmc
import  xbmcaddon
import  xbmcgui

from    util.temperature                import  Temperature
import  vera.device
from    gui.xbmc                        import  *
import  gui.controlid                   as      controlid
import  gui.controlid.dimmable_light

__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

DIMMING_INTERVAL = 0.25

class DimLightThread( threading.Thread ):

    def __init__(self, gui_):
        threading.Thread.__init__(self)
        self.gui = gui_
        self.device = gui_.device
        self.vera = gui_.parent.vera

    def run(self):
        self.runThread = True
        slider = self.gui.getControl(controlid.dimmable_light.SLIDER)
        while(self.runThread):
            newValue = slider.getPercent()
            if newValue != int( float( self.device['level'] ) ): 
                try:
                    vera.device.dim(self.device, self.vera, newValue)
                except socket.error as e:
                    msg = 'socket: %s' % e.__str__()
                    error_dialog = xbmcgui.Dialog()
                    error_dialog.ok( 'Network Connection Error', msg ) 
                    self.runThread = False
            time.sleep(DIMMING_INTERVAL)

class DimmableLight( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.dimmerThread = DimLightThread(self)

    def onInit(self):
        self.slider().setPercent( int( float( self.device['level'] ) ) )
        self.dimmerThread.start()

    def slider(self):
        return self.getControl(controlid.dimmable_light.SLIDER)

    def onAction(self, action):
        if action in (ACTION_MOVE_LEFT, ACTION_MOVE_RIGHT):
            xbmc.enableNavSounds(False)
        else:
            xbmc.enableNavSounds(True)

        if action in (ACTION_PREVIOUS_MENU, ACTION_ENTER):
            self.dimmerThread.runThread = False
            self.close()
        elif action == ACTION_MOVE_UP:
            self.slider().setPercent(100)
        elif action == ACTION_MOVE_DOWN:
            self.slider().setPercent(0)

gui.popup.DimmableLight = DimmableLight
