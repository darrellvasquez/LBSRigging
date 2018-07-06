import maya.cmds as cmds
import json
import tempfile
import os

def writeJson(fileName, rig_data):
	with open(fileName, 'w') as outfile:
		json.dump(rig_data, outfile)
	file.close(outfile)

def readJson(fileName):
	with open(fileName, "r") as infile:
		rig_data = (open(infile.name, 'r').read())
	return rig_data


def createJoint(name, position, instance):
	#use a list comprehension to build joints
	JNT_list = [cmds.joint(n=name[i].replace('s_', instance), p=position[i]) for i in range(len(name))]
	cmds.select(d=True)
	return(JNT_list)


def createControl(ctrlInfo):
	control_info = []
	for info in ctrlInfo:
		print info
		#Create IK/FK Controls
		#get world space position of wrist
		pos = info[0]
		#Create circle control object
		ctrl = cmds.circle(n=info[1], nr=(0, 0, 1), c=(0, 0, 0))
		#Create empty group
		ctrlGRP = cmds.group(em=True, name=info[1] + "_GRP" )
		#parent control to group
		cmds.parent(ctrl, ctrlGRP)
		#move group to joint
		cmds.xform(ctrlGRP, t=pos, ws=True)
		control_info.append([ctrlGRP, ctrl])
	return(control_info)


def calculatePVposition(jnts):
	from maya import cmds , OpenMaya
	start = cmds.xform(jnts[0], q=True, ws=True, t=True)
	mid = cmds.xform(jnts[1], q=True, ws=True, t=True)
	end = cmds.xform(jnts[2], q=True, ws=True, t=True)
	startV = OpenMaya.MVector(start[0] ,start[1],start[2])
	midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
	endV = OpenMaya.MVector(end[0] ,end[1],end[2])
	startEnd = endV - startV
	startMid = midV - startV
	dotP = startMid * startEnd
	proj = float(dotP) / float(startEnd.length())
	startEndN = startEnd.normal()
	projV = startEndN * proj
	arrowV = startMid - projV
	arrowV*= 10.0
	finalV = arrowV + midV
	return ([finalV.x , finalV.y , finalV.z])


def connectThroughBC(parentsA, parentsB, children, instance, switchattr ):
	constraints = []
	for j in range(len(children)):
		switchPrefix = children[j].partition('_')[2]
		bcNodeT = cmds.shadingNode("blendColors", asUtility=True, n='bcNodeT_switch_' + switchPrefix)
		cmds.connectAttr(switchattr, bcNodeT  + '.blender')
		bcNodeR = cmds.shadingNode("blendColors", asUtility=True, n='bcNodeR_switch_' + switchPrefix)
		cmds.connectAttr(switchattr, bcNodeR  + '.blender')
		bcNodeS = cmds.shadingNode("blendColors", asUtility=True, n='bcNodeS_switch_' + switchPrefix)
		cmds.connectAttr(switchattr, bcNodeS  + '.blender')
		constraints.append([bcNodeT, bcNodeR, bcNodeS])
		# Input Parents
		cmds.connectAttr(parentsA[j] + '.translate', bcNodeT + '.color1')
		cmds.connectAttr(parentsA[j] + '.rotate', bcNodeR + '.color1')
		cmds.connectAttr(parentsA[j] + '.scale', bcNodeS + '.color1')
		if parentsB != 'None':
			cmds.connectAttr(parentsB[j] + '.translate', bcNodeT + '.color2')
			cmds.connectAttr(parentsB[j] + '.rotate', bcNodeR + '.color2')
			cmds.connectAttr(parentsB[j] + '.scale', bcNodeS + '.color2')
		# Output to Children
		cmds.connectAttr(bcNodeT + '.output', children[j] + '.translate')
		cmds.connectAttr(bcNodeR + '.output', children[j] + '.rotate')
		cmds.connectAttr(bcNodeS + '.output', children[j] + '.scale')
	return constraints

#IKFK Match
def match_IKFK(*args):
    print "Match"
    initializesj = cmds.scriptJob(runOnce=False, kws=False, e=["SelectionChanged", checkForSwitch])

def checkForSwitch(*args):
    print "Check"
    sel = cmds.ls(sl=True)[0]
    print sel
    print cmds.listAttrs(sel, k=True)
    if ".IK_FK" in cmds.listAttrs(cmds.ls(sl=True)[0], k=True):
        print "Has Switch"

def setupMatchScripts(*args):
    # Look for controls with IK_FK attributes and set scriptJobs on them.
    print "Setup Match"