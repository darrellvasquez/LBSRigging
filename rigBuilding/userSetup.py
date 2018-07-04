import os
import sys
import maya.cmds as cmds



sys.path.append('D:/Dropbox/lb_tools/LBS_Rigging/rigBuilding/')
cmds.evalDeferred('import startup')
#end user startup

print "In User Setup"

eval(“source \“C:/Users/Public/Pixologic/GoZApps/Maya/GoZBrushToMaya.mel\””);

