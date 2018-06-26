import os
import sys
import maya.cmds as cmds

print "In User Setup"

sys.path.append('D:/Dropbox/lb_tools/LBS_Rigging/rigBuilding/')
cmds.evalDeferred('import startup')
#end user startup

