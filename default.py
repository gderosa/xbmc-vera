
import sys
import os
import xbmcaddon


__scriptname__ = "Vera Home Automation"
__author__     = "VEMAR s.a.s."
__GUI__        = "VEMAR s.a.s."
__scriptId__   = "script.vera"
__settings__   = xbmcaddon.Addon(id=__scriptId__)
__language__   = __settings__.getLocalizedString
__version__    = __settings__.getAddonInfo("version")
__cwd__        = __settings__.getAddonInfo('path')


BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __cwd__, "resources", "lib" ) )
sys.path.append (BASE_RESOURCE_PATH)


import gui

ui = gui.GUI( "%s.xml" % __scriptId__.replace(".","-") , __cwd__, "Default")
ui.doModal()
del ui


