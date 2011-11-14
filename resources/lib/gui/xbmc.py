# import xbmcgui

# See xbmc/guilib/Key.h in XMBC sources

ACTION_MOVE_LEFT            =     1
ACTION_MOVE_RIGHT           =     2
ACTION_MOVE_UP              =     3
ACTION_MOVE_DOWN            =     4
ACTION_ENTER                =     7
ACTION_PREVIOUS_MENU        =    10

ACTION_MOUSE_START          =   100
ACTION_MOUSE_LEFT_CLICK     =   100
ACTION_MOUSE_RIGHT_CLICK    =   101
ACTION_MOUSE_MIDDLE_CLICK   =   102
ACTION_MOUSE_DOUBLE_CLICK   =   103
ACTION_MOUSE_WHEEL_UP       =   104
ACTION_MOUSE_WHEEL_DOWN     =   105
ACTION_MOUSE_DRAG           =   106
ACTION_MOUSE_MOVE           =   107
ACTION_MOUSE_END            =   109

ACTION_MOUSE_CLICK = (
    ACTION_MOUSE_LEFT_CLICK, 
    ACTION_MOUSE_RIGHT_CLICK, 
    ACTION_MOUSE_MIDDLE_CLICK,
    ACTION_MOUSE_DOUBLE_CLICK,
)
ACTION_MOUSE_WHEEL = (
    ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_WHEEL_DOWN,
)

## 0xE000 -> 0xE0FF is reserved for mouse actions
#KEY_MOUSE               = 0xE000
#
#def isMouse(action):
#    return (action.getId() & 0xFF00 == KEY_MOUSE) 


