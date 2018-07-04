import maya.cmds as cmds
import json
import os
import system.utils as utils


class Rig_Limb:
	def __init__(self):
		#Get our joint lists from a json file.
		print os.environ["LBS_DATA"]
		data_path = os.environ["LBS_DATA"] + 'arm_data.json'
		#Use our readJson function
		data = utils.readJson(data_path)
		#Load the json into a dictionary
		self.module_info = json.loads(data)
		""" NOTE: If we wanted to build our arm from some set of joints
		in the scene, we could overwrite self.module_info['positions']"""


	def rig_limb(self):
		#Create IK Joints
		self.createJoint(self.module_info['IKjoints'])
		cmds.select(d=True)
		#Create FK Joints
		self.createJoint(self.module_info['FKjoints'])
		cmds.select(d=True)
		#Create RIG Joints
		self.createJoint(self.module_info['RIGjoints'])
		cmds.select(d=True)

		#Create IK Rig
		#IK Handle
		IKhandle = cmds.ikHandle(n=(self.module_info['IKcontrols'][1]), sj=(self.module_info['IKjoints'][0]), ee=(self.module_info['IKjoints'][2]), p=2, w=1)

		self.createControl([[self.module_info['position'][2], self.module_info['IKcontrols'][2]]])

		PVpos = self.calculatePVposition([self.module_info['IKjoints'][0], self.module_info['IKjoints'][1], self.module_info['IKjoints'][2]])
		PVctrlInfo = [[PVpos, self.module_info['IKcontrols'][0]]]
		self.createControl(PVctrlInfo)

		#parent ikHandle to ctrl
		cmds.parent(self.module_info['IKcontrols'][1], self.module_info['IKcontrols'][2])

		#PV constraint
		cmds.poleVectorConstraint(self.module_info['IKcontrols'][0], self.module_info['IKcontrols'][1])

		#orient constraint arm ik_wrist to wrist_ctrl
		cmds.orientConstraint(self.module_info['IKcontrols'][2], self.module_info['IKcontrols'][0], mo=True)

		#Create FK rig
		FKctrlInfo = self.createControl([[self.module_info['position'][2], self.module_info['FKcontrols'][2]],
		[self.module_info['position'][1], self.module_info['FKcontrols'][1]],
		[self.module_info['position'][0], self.module_info['FKcontrols'][0]]])

		#Parent FK controls
		cmds.parent(FKctrlInfo[1][2], FKctrlInfo[0][1])
		cmds.parent(FKctrlInfo[2][2], FKctrlInfo[1][1])


    
	def createJoint(self, jointInfo):
	    for i in range(len(jointInfo)):
			cmds.joint(n=jointInfo[i], p=self.module_info['position'][i])


	def createControl(self, ctrlInfo):
		control_info = []
		for info in ctrlInfo:
			#Create IK/FK Controls
			#get world space position of wrist
			pos = info[0]
			#Create empty group
			ctrlGRP = cmds.group(em=True, name=info[1] + "_GRP" )
			#Create circle control object
			ctrl = cmds.circle(n=info[1], nr=(0, 0, 1), c=(0, 0, 0) )
			#parent control to group
			cmds.parent(ctrl, ctrlGRP)
			#move group to joint
			cmds.xform(ctrlGRP, t=pos, ws=True)
			control_info.append([ctrlGRP, ctrl])
			return(control_info)

	def calculatePVposition(self, jnts):
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
		arrowV*= 0.5
		finalV = arrowV + midV
		return ([finalV.x , finalV.y , finalV.z])