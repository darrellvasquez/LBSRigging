import maya.cmds as cmds
import json
import os
import system.utils as utils

#We can use variables above the class level that can be read on the class import
#This is also known as a attribute of a class
className = 'Rig_Arm'
layoutFile = 'arm_data.json'
numberJNTS = 3

class Rig_Arm:
	def __init__(self):
		#Get our joint lists from a json file.
		print os.environ["LBS_DATA"]
		data_path = os.environ["LBS_DATA"] + 'data/arm_data.json'
		#Use our readJson function
		data = utils.readJson(data_path)
		#Load the json into a dictionary
		self.module_info = json.loads(data)
		""" NOTE: If we wanted to build our arm from some set of joints
		in the scene, we could overwrite self.module_info['positions']"""

		# Make a new dictionary to store information about the arg rig (layout rig)
		self.rig_info = {}

		# Here we will see if we have a selection to get new positions from.
		if len(cmds.ls(sl=True, type='joint')) == numberJNTS :
			sel=cmds.ls(sl=True, type='joint')
			position = []
			for s in sel:
				position.append(cmds.xform(s, q=True, ws=True, t=True))
			self.rig_info['position'] = position

		else:
			self.rig_info['position'] = self.module_info['position']

		""" Instead of the else:, we could just return a message that the selection
		does not meet the requirements for an arm. """

		""" what if we want a LF and a RT arm/leg? For now we will set
		a temp variable to override the name, but later we will build
		this into the UI. """

		self.instance = 'LF_'

		#Run rig_arm function
		self.rig_arm()


	def rig_arm(self):
		cmds.select(d=True)
		#Create IK Joints
		self.rig_info['IKjoints'] = utils.createJoint(self.module_info['IKjoints'], self.rig_info['position'], self.instance)
		
		#Create FK Joints
		self.rig_info['FKjoints'] = utils.createJoint(self.module_info['FKjoints'], self.rig_info['position'], self.instance)
		
		#Create RIG Joints
		self.rig_info['RIGjoints'] = utils.createJoint(self.module_info['RIGjoints'], self.rig_info['position'], self.instance)

		#Create IK Rig
		#IK Handle
		#IKcontrols': ["s_armPV_CTRL", "s_arm_ikHandle", "s_armIK_CTRL"]
		ikHandleName = self.module_info['IKcontrols'][1].replace('s_', self.instance)
		self.rig_info['IKhandle'] = cmds.ikHandle(n=ikHandleName, sj=self.rig_info['IKjoints'][0], ee=self.rig_info['IKjoints'][2], p=2, w=1 )

		self.rig_info['IKcontrols'] = utils.createControl([[self.rig_info['position'][2], self.rig_info['IKcontrols'][2]]])

		PVpos = utils.calculatePVposition([self.rig_info['IKjoints'][0], self.rig_info['IKjoints'][1], self.rig_info['IKjoints'][2]])
		PVctrlInfo = [[PVpos, self.rig_info['IKcontrols'][0]]]
		utils.createControl(PVctrlInfo)

		# Make a control for arm settings
		self.rig_info['setcontrol']=utils.createControl([[self.rig_info['positions'][2], 'ctrl_settings']])[0]
		cmds.addAttr(self.rig_info['setcontrol'][1], ln='IK_FK', at="enum", en="FK:IK:", k=True )

		#parent ikHandle to ctrl
		cmds.parent(self.rig_info['IKhandle'][1], self.rig_info['IKcontrols'][2])

		#PV constraint
		cmds.poleVectorConstraint(self.rig_info['IKcontrols'][0], self.rig_info['IKcontrols'][1])

		#orient constraint arm ik_endArm to endArm_ctrl
		cmds.orientConstraint(self.rig_info['IKcontrols'][2], self.rig_info['IKcontrols'][0], mo=True)

		#Create FK rig
		self.rig_info['FKcontrols'] = utils.createControl([[self.rig_info['position'][2], self.rig_info['FKcontrols'][2]],
		[self.rig_info['position'][1], self.rig_info['FKcontrols'][1]],
		[self.rig_info['position'][0], self.rig_info['FKcontrols'][0]]])

		#Parent FK controls
		cmds.parent(self.rig_info[2][0], self.rig_info[1][1])
		cmds.parent(self.rig_info[1][0], self.rig_info[0][1])

		#Constraint upArm
		cmds.pointConstraint( self.rig_info['FKcontrols'][0], self.rig_info['FKjoints'][0] )
		cmds.orientConstraint( self.rig_info['FKcontrols'][0], self.rig_info['FKjoints'][0] )
		cmds.select(d=True)

		#Constraint loArm
		cmds.pointConstraint( self.rig_info['FKcontrols'][1], self.rig_info['FKjoints'][1] )
		cmds.orientConstraint( self.rig_info['FKcontrols'][1], self.rig_info['FKjoints'][1] )
		cmds.select(d=True)

		#Constraint wrist
		cmds.pointConstraint( self.rig_info['FKcontrols'][2], self.rig_info['FKjoints'][2] )
		cmds.orientConstraint( self.rig_info['FKcontrols'][2], self.rig_info['FKjoints'][2] )
		cmds.select(d=True)

		# Connect Ik and Fk to Rig joints
		switchattr = self.rig_info['setcontrol'][1] + '.IK_FK'
		utils.connectThroughBC(self.rig_info['IKjoints'], self.rig_info['FKjoints'], self.rig_info['RIGjoints'], self.instance, switchattr )