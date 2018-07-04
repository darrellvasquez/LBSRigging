import maya.cmds as cmds

print "UI"

class LBS_UI:

	def __init__(self, *args):
		print 'In LBS_UI'
		mi = cmds.window('MayaWindow', ma=True, q=True)
		for m in mi:
			if m == 'LBS_menu':
				cmds.deleteUI('LBS_menu', m=True)

		myMenu = cmds.menu('LBS_menu', label='LBSMenu', to=True, p='MayaWindow')
		cmds.menuItem(label='Rig Tool', p=myMenu, command=self.ui)

		""" Create a dictionary to store UI elements.
		This will allow us to access these elements later."""
		self.UIElements = {}

	def ui(self, *args):
		"""Check to see if UI exists """
		windowName = "Window"
		if cmds.window(windowName, exists=True):
			cmds.deleteUI(windowName)
		""" define width and height for buttons and windows"""
		windowWidth = 480
		windowHeight = 80
		buttonWidth = 100
		buttonHeight = 30

		self.UIElements["window"] = cmds.window(windowName, width=windowWidth, height=windowHeight, title="LBS_UI", sizeable=True)

		self.UIElements["mainColLayout"] = cmds.columnLayout(adjustableColumn=True)
		self.UIElements["guiiFrameLayout1"] = cmds.frameLayout( label='layout', borderStyle='in', p=self.UIElements["mainColLayout"])
		self.UIElements["guiiFlowLayout1"] = cmds.flowLayout(v=False, width=windowWidth, height=windowHeight/2, wr=True, bgc=[0.2, 0.2, 0.2], p=self.UIElements["guiiFrameLayout1"])

		#Menu listing all the layout files.
		cmds.separator(w=10, hr=True, st='none',p=self.UIElements["guiiFlowLayout1"])
		self.UIElements["rig_button"] = cmds.button(label='rig arm', width=buttonWidth, height=buttonHeight, bgc=[0.2, 0.4, 0.2], p=self.UIElements["guiiFlowLayout1"], c=self.rigLimb)

		"""show the Window"""
		cmds.showWindow(windowName)

	def rigLimb(*args):
		print "Rig_Limb"
		import rig.rig_limb as rig_limb
		rig_limb = rig_limb.Rig_Limb()
		rig_limb.rig_limb()