import xbmc
import xbmcgui

class GUI( xbmcgui.WindowXML ):
    def __init__( self, *args, **kwargs ):
        pass

    def onInit(self):
        print "vera: GUI.onInit"
        label = xbmcgui.ControlLabel(100,100,100,100,'VAFFA');
        self.addControl(label)


