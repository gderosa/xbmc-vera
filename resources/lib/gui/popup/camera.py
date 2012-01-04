import  xbmcaddon
import  xbmcgui

from    gui                         import controlid
from    gui.xbmc                    import *
import  gui.popup
import  gui.controlid.camera


__addon__   = xbmcaddon.Addon('script.vera')
__cwd__     = __addon__.getAddonInfo('path')

class Camera( xbmcgui.WindowXMLDialog ):

    def __init__(self, *args, **kwargs):
        self.device = kwargs['device']
        self.parent = kwargs['parent']
        self.vera   = self.parent.vera

    def onInit(self):
        self.update()

    def onAction(self, action):
        if      action == ACTION_PREVIOUS_MENU:
            self.close()
        elif    action == ACTION_ENTER:
            self.close()

    def update(self):
        self.image().setImage(u"http://192.168.0.27:3480/data_request?id=cam_image&Device_Num=64")

    def image(self):
        return self.getControl(controlid.camera.IMAGE)



# Compat
gui.popup.Camera = Camera
