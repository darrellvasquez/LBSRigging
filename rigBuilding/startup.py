import maya.cmds as cmds
import os
import sys

print "Startup"

#Set a system path for data files.
os.environ["LBS_DATA"] = 'D:/Dropbox/lb_tools/LBS_Rigging/rigBuilding/data/'

import myui.myui as ui
#still need to figure out what this is
ui.LBS_UI()