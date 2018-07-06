import maya.cmds as cmds

#Create arm joints
#Create IK joints
IKjointInfo = [['IK_upArm_JNT', [0, 0, 0]], ['IK_loArm_JNT', [-1, 0, -3]], ['IK_wristArm_JNT', [0, 0, -6]], ['IK_wristArmEnd_JNT', [0, 0, -8]]]
#Create FK joints
FKjointInfo = [['FK_upArm_JNT', [0, 0, 0]], ['FK_loArm_JNT', [-1, 0, -3]], ['FK_wristArm_JNT', [0, 0, -6]], ['FK_wristArmEnd_JNT', [0, 0, -8]]]
#Create rig joints    
RIGjointInfo = [['RIG_upArm_JNT', [0, 0, 0]], ['RIG_loArm_JNT', [-1, 0, -3]], ['RIG_wristArm_JNT', [0, 0, -6]], ['RIG_wristArmEnd_JNT', [0, 0, -8]]]


class Rig_Limb:
	def rig_limb(self):
		#Create IK Joints
		self.createJoint(IKjointInfo)
		cmds.select(d=True)
		#Create FK Joints
		self.createJoint(FKjointInfo)
		cmds.select(d=True)
		#Create RIG Joints
		self.createJoint(RIGjointInfo)
		cmds.select(d=True)

		#Create IK Rig
		#IK Handle
		IKhandle = cmds.ikHandle(n='IK_wrist_handle', sj='IK_upArm_JNT', ee='IK_wristArm_JNT', p=2, w=1)

		IKctrlInfo = [[IKjointInfo[2][1], 'IK_wrist_CTRL', 'IK_wrist_GRP']]
		self.createControl(IKctrlInfo)

		PVpos = self.calculatePVposition([IKjointInfo[0][0], IKjointInfo[1][0], IKjointInfo[2][0]])
		PVctrlInfo = [[PVpos, 'PV_arm_CTRL', 'PV_arm_GRP']]
		self.createControl(PVctrlInfo)

		#parent ikHandle to ctrl
		cmds.parent('IK_wrist_handle', 'IK_wrist_CTRL')

		#PV constraint
		cmds.poleVectorConstraint(PVctrlInfo[0][1], IKhandle[0])

		#orient constraint arm ik_wrist to wrist_ctrl
		cmds.orientConstraint(IKctrlInfo[0][1], IKjointInfo[2][0], mo=True)

		#Create FK rig
		FKctrlInfo = [[FKjointInfo[0][1], 'FK_upArm_CTRL', 'FK_upArm_GRP'], [FKjointInfo[1][1], 'FK_loArm_CTRL', 'FK_loArm_GRP'], [FKjointInfo[2][1], 'FK_wrist_CTRL', 'FK_wrist_GRP']]
		self.createControl(FKctrlInfo)

		#Parent FK controls
		cmds.parent(FKctrlInfo[1][2], FKctrlInfo[0][1])
		cmds.parent(FKctrlInfo[2][2], FKctrlInfo[1][1])

    
	def createJoint(self, jointInfo):
	    for item in jointInfo:
	        cmds.joint(n=item[0], p=item[1])
	        

	def createControl(self, ctrlInfo):
		for info in ctrlInfo:
	    		#Create IK Control
	    		#get world space position of wrist
	    		pos = info[0]
	    		#Create empty group
	    		ctrlGrp = cmds.group(em=True, name=info[2])
	    		#Create circle control object
	    		ctrl = cmds.circle(n=info[1], nr=(0, 0, 1), c=(0, 0, 0))
	    		#parent control to group
	    		cmds.parent(ctrl, ctrlGrp)
	    		#move group to joint
	    		cmds.xform(ctrlGrp, t=pos, ws=True)

	def calculatePVposition(self, jnts):
		from maya import cmds , OpenMaya
		start = cmds.xform(jnts[0], q=True, ws=True, t=True)
		mid = cmds.xform(jnts[1], q=True, ws=True, t=True)
		end = cmds.xform(jnts[2], q=True, ws=True, t=True)
		startV = openMaya.MVector(start[0] ,start[1],start[2])
		midV = openMaya.MVector(mid[0] ,mid[1],mid[2])
		endV = openMaya.MVector(end[0] ,end[1],end[2])
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