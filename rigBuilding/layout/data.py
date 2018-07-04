#Create arm joints
#Create IK joints
IKjointInfo = [['IK_upArm_JNT', [0, 0, 0]], ['IK_loArm_JNT', [-1, 0, -3]], ['IK_wristArm_JNT', [0, 0, -6]], ['IK_wristArmEnd_JNT', [0, 0, -8]]]
#Create FK joints
FKjointInfo = [['FK_upArm_JNT', [0, 0, 0]], ['FK_loArm_JNT', [-1, 0, -3]], ['FK_wristArm_JNT', [0, 0, -6]], ['FK_wristArmEnd_JNT', [0, 0, -8]]]
#Create rig joints    
RIGjointInfo = [['RIG_upArm_JNT', [0, 0, 0]], ['RIG_loArm_JNT', [-1, 0, -3]], ['RIG_wristArm_JNT', [0, 0, -6]], ['RIG_wristArmEnd_JNT', [0, 0, -8]]]

rig_data = {}
rig_data['IKjoints'] = ['IK_upArm_JNT', 'IK_loArm_JNT','IK_wristArm_JNT', 'IK_wristArmEnd_JNT']
rig_data['FKjoints'] = ['FK_upArm_JNT', 'FK_loArm_JNT','FK_wristArm_JNT', 'FK_wristArmEnd_JNT']
rig_data['RIGjoints'] = ['RIG_upArm_JNT', 'RIG_loArm_JNT','RIG_wristArm_JNT', 'RIG_wristArmEnd_JNT']
rig_data['BNDjoints'] = ['BND_upArm_JNT', 'BND_loArm_JNT','BND_wristArm_JNT', 'BND_wristArmEnd_JNT']
rig_data['IKcontrols'] = ['PV_arm_CTRL', 'IK_wrist_handle', 'IK_wrist_CTRL']
rig_data['FKcontrols'] = ['FK_upArm_CTRL', 'FK_loArm_CTRL', 'FK_wrist_CTRL']
rig_date['position'] = [[0, 0, 0], [-1, 0, -3], [0, 0, -6], [0, 0, -8]]