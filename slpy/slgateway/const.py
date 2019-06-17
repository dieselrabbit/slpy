import sys
import os
import struct

def me(): return(os.path.basename(sys.argv[0]))

class header:
  fmt    = "<HHI"
  length = struct.calcsize(fmt)

# Some of the message codes as documented in Sections 4 and 5 of the above PDF.
class code:
  MSG_CODE_1        = 0
  UNKNOWN_ANSWER    = 13
  CHALLENGE_QUERY   = 14
  CHALLENGE_ANSWER  = CHALLENGE_QUERY  + 1
  LOCALLOGIN_QUERY  = 27
  LOCALLOGIN_ANSWER = LOCALLOGIN_QUERY + 1
  VERSION_QUERY     = 8120
  VERSION_ANSWER    = VERSION_QUERY    + 1
  POOLSTATUS_QUERY  = 12526
  POOLSTATUS_ANSWER = POOLSTATUS_QUERY + 1
  BUTTONPRESS_QUERY = 12530
  BUTTONPRESS_ANSWER = BUTTONPRESS_QUERY + 1
  CTRLCONFIG_QUERY  = 12532
  CTRLCONFIG_ANSWER = CTRLCONFIG_QUERY + 1

class mapping:
  BODY_TYPE  = ['Pool', 'Spa']
  HEAT_MODE  = ['Off', 'Solar', "Solar Prefered", 'Heat', "Don't Change"]
  ON_OFF     = ['Off', 'On']
  COLOR_MODE = ['Off', 'On', 'Set', 'Sync', 'Swim', 'Party', 'Romantic', 'Caribbean', 'American', 'Sunset', 'Royal', 'Save', 'Recall', 'Blue', 'Green', 'Red', 'White', 'Magenta', 'Thumper', 'Next', 'Reset', 'Hold']
