#Create arm joints
#Create IK joints
IKjointInfo = (['IK_upArm_JNT', [0, 0, 0]], ['IK_loArm_JNT', [-1, 0, -3]], ['IK_wristArm_JNT', [0, 0, -6]], ['IK_wristArmEnd_JNT', [0, 0, -8]])
print IKjointInfo

for item in IKjointInfo:
    cmds.joint( n=item[0], p=item[1] )
cmds.select( d=True )
    
#Create FK joints    
FKjointInfo = (['FK_upArm_JNT', [0, 0, 0]], ['FK_loArm_JNT', [-1, 0, -3]], ['FK_wristArm_JNT', [0, 0, -6]], ['FK_wristArmEnd_JNT', [0, 0, -8]])
print FKjointInfo

for item in FKjointInfo:
    cmds.joint( n=item[0], p=item[1] )
cmds.select( d=True )

#Create rig joints    
RIGjointInfo = (['RIG_upArm_JNT', [0, 0, 0]], ['RIG_loArm_JNT', [-1, 0, -3]], ['RIG_wristArm_JNT', [0, 0, -6]], ['RIG_wristArmEnd_JNT', [0, 0, -8]])
print RIGjointInfo

for item in RIGjointInfo:
    cmds.joint( n=item[0], p=item[1] )
cmds.select( d=True )



#Create IK RIG
#Get Position of WristArm joint
wristPos = cmds.xform( 'IK_wristArm_JNT', q=True, ws=True, t=True )
#Create IK Handle
cmds.ikHandle( n='IK_wrist_ikHandle', sj='IK_upArm_JNT', ee='IK_wristArm_JNT', p=2, w=1 )
#Create IK Handle Group
cmds.group( n='IK_wrist_GRP', em=True )
#Create IK Control
cmds.circle( n='IK_wrist_CTRL', nr=(0, 0, 1), c=(0, 0, 0) )
#Change Color
cmds.setAttr( 'IK_wrist_CTRLShape.overrideEnabled', 1 )
cmds.setAttr( 'IK_wrist_CTRLShape.overrideColor', 12) 
#Parent Control/Group
cmds.parent( 'IK_wrist_CTRL', 'IK_wrist_GRP' )
#move Wrist group to wrist position
cmds.xform( 'IK_wrist_GRP', t=wristPos, ws=True )
#Parent IK handle to IK control
cmds.parent( 'IK_wrist_ikHandle', 'IK_wrist_CTRL' )

#Create IK PV
#Get loArm Position
loArmPos = cmds.xform( 'IK_loArm_JNT', q=True, ws=True, t=True )
#Create PV Group
cmds.group( n='IK_PV_GRP', em=True )
#Create IK Control
cmds.circle( n='IK_PV_CTRL', nr=(0, 1, 0), c=(0, 0, 0) )
#Change Color
cmds.setAttr( 'IK_PV_CTRLShape.overrideEnabled', 1 )
cmds.setAttr( 'IK_PV_CTRLShape.overrideColor', 12) 
#Parent Control/Group
cmds.parent( 'IK_PV_CTRL', 'IK_PV_GRP' )
#move Wrist group to wrist position
cmds.xform( 'IK_PV_GRP', t=loArmPos, ws=True )
cmds.setAttr( 'IK_PV_GRP.tx', -1 -4)
#Constraint PV
cmds.poleVectorConstraint( 'IK_PV_CTRL', 'IK_wrist_ikHandle' )



#Create FK Rig
#Get upArm Position
upArmPos = cmds.xform( 'FK_upArm_JNT', q=True, ws=True, t=True )
#Create upArm Group
cmds.group( n='FK_upArm_GRP', em=True )
#Create upArm FK Control
cmds.circle( n='FK_upArm_CTRL', nr=(0, 1, 0), c=(0, 0, 0) )
#Change Color
cmds.setAttr( 'FK_upArm_CTRLShape.overrideEnabled', 1 )
cmds.setAttr( 'FK_upArm_CTRLShape.overrideColor', 12) 
#Parent Control/Group
cmds.parent( 'FK_upArm_CTRL', 'FK_upArm_GRP' )
#move upArm group to upArm position
cmds.xform( 'FK_upArm_GRP', t=upArmPos, ws=True )
#Constraint upArm
cmds.pointConstraint( 'FK_upArm_CTRL', 'FK_upArm_JNT' )
cmds.orientConstraint( 'FK_upArm_CTRL', 'FK_upArm_JNT' )
cmds.select(d=True)

#Get loArm Position
loArmPos = cmds.xform( 'FK_loArm_JNT', q=True, ws=True, t=True )
#Create loArm Group
cmds.group( n='FK_loArm_GRP', em=True )
#Create loArm FK Control
cmds.circle( n='FK_loArm_CTRL', nr=(0, 1, 0), c=(0, 0, 0) )
#Change Color
cmds.setAttr( 'FK_loArm_CTRLShape.overrideEnabled', 1 )
cmds.setAttr( 'FK_loArm_CTRLShape.overrideColor', 12) 
#Parent Control/Group
cmds.parent( 'FK_loArm_CTRL', 'FK_loArm_GRP' )
#move loArm group to loArm position
cmds.xform( 'FK_loArm_GRP', t=loArmPos, ws=True )
#Constraint loArm
cmds.pointConstraint( 'FK_loArm_CTRL', 'FK_loArm_JNT' )
cmds.orientConstraint( 'FK_loArm_CTRL', 'FK_loArm_JNT' )
cmds.select(d=True)

#Get wristArm Position
wristArmPos = cmds.xform( 'FK_wristArm_JNT', q=True, ws=True, t=True )
#Create wristArm Group
cmds.group( n='FK_wristArm_GRP', em=True )
#Create wristArm FK Control
cmds.circle( n='FK_wristArm_CTRL', nr=(0, 1, 0), c=(0, 0, 0) )
#Change Color
cmds.setAttr( 'FK_wristArm_CTRLShape.overrideEnabled', 1 )
cmds.setAttr( 'FK_wristArm_CTRLShape.overrideColor', 12) 
#Parent Control/Group
cmds.parent( 'FK_wristArm_CTRL', 'FK_wristArm_GRP' )
#move wristArm group to wristArm position
cmds.xform( 'FK_wristArm_GRP', t=wristArmPos, ws=True )
#Constraint wristArm
cmds.pointConstraint( 'FK_wristArm_CTRL', 'FK_wristArm_JNT' )
cmds.orientConstraint( 'FK_wristArm_CTRL', 'FK_wristArm_JNT' )
cmds.select(d=True)

#Parent FK Controls
cmds.parent( 'FK_wristArm_GRP', 'FK_loArm_CTRL' )
cmds.parent( 'FK_loArm_GRP', 'FK_upArm_CTRL' )
cmds.select( d=True)

#creat controls group and group controls to controls group
cmds.select('IK_wrist_GRP', 'IK_PV_GRP', 'FK_upArm_GRP' )
cmds.group(n='controls')



#Use BlendColor Node to Constrain IK/FK joints to Rig joints
#Create upArm blend Color node
bcNodeT = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_upArmSwitchT_blendColor')
bcNodeR = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_upArmSwitchR_blendColor')
bcNodeS = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_upArmSwitchS_blendColor')
# Input1 Parents
cmds.connectAttr('FK_upArm_JNT.translate', bcNodeT + '.color1')
cmds.connectAttr('FK_upArm_JNT.rotate', bcNodeR + '.color1')
cmds.connectAttr('FK_upArm_JNT.scale', bcNodeS + '.color1')
# Input2 Parents
cmds.connectAttr('IK_upArm_JNT.translate', bcNodeT + '.color2')
cmds.connectAttr('IK_upArm_JNT.rotate', bcNodeR + '.color2')
cmds.connectAttr('IK_upArm_JNT.scale', bcNodeS + '.color2')
# Output Parents
cmds.connectAttr(bcNodeT + '.output', 'RIG_upArm_JNT.translate')
cmds.connectAttr(bcNodeR + '.output', 'RIG_upArm_JNT.rotate')
cmds.connectAttr(bcNodeS + '.output', 'RIG_upArm_JNT.scale')

#Create loArm blend Color node
bcNodeT = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_loArmSwitchT_blendColor')
bcNodeR = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_loArmSwitchR_blendColor')
bcNodeS = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_loArmSwitchS_blendColor')
# Input1 Parents
cmds.connectAttr('FK_loArm_JNT.translate', bcNodeT + '.color1')
cmds.connectAttr('FK_loArm_JNT.rotate', bcNodeR + '.color1')
cmds.connectAttr('FK_loArm_JNT.scale', bcNodeS + '.color1')
# Input2 Parents
cmds.connectAttr('IK_loArm_JNT.translate', bcNodeT + '.color2')
cmds.connectAttr('IK_loArm_JNT.rotate', bcNodeR + '.color2')
cmds.connectAttr('IK_loArm_JNT.scale', bcNodeS + '.color2')
# Output Parents
cmds.connectAttr(bcNodeT + '.output', 'RIG_loArm_JNT.translate')
cmds.connectAttr(bcNodeR + '.output', 'RIG_loArm_JNT.rotate')
cmds.connectAttr(bcNodeS + '.output', 'RIG_loArm_JNT.scale')

#Create wristArm blend Color node
bcNodeT = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_wristArmSwitchT_blendColor')
bcNodeR = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_wristArmSwitchR_blendColor')
bcNodeS = cmds.shadingNode("blendColors", asUtility=True, n='IK_FK_wristArmSwitchS_blendColor')
# Input1 Parents
cmds.connectAttr('FK_wristArm_JNT.translate', bcNodeT + '.color1')
cmds.connectAttr('FK_wristArm_JNT.rotate', bcNodeR + '.color1')
cmds.connectAttr('FK_wristArm_JNT.scale', bcNodeS + '.color1')
# Input2 Parents
cmds.connectAttr('IK_wristArm_JNT.translate', bcNodeT + '.color2')
cmds.connectAttr('IK_wristArm_JNT.rotate', bcNodeR + '.color2')
cmds.connectAttr('IK_wristArm_JNT.scale', bcNodeS + '.color2')
# Output Parents
cmds.connectAttr(bcNodeT + '.output', 'RIG_wristArm_JNT.translate')
cmds.connectAttr(bcNodeR + '.output', 'RIG_wristArm_JNT.rotate')
cmds.connectAttr(bcNodeS + '.output', 'RIG_wristArm_JNT.scale')