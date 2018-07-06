import maya.cmds as cmds
import os
import system.utils as utils
from functools import partial
 
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
 
        # This dictionary will store all of the available rigging modules used.
        self.rigModList = []
        rigContents = os.listdir(os.environ["LBS_DATA"] + 'rig/')
        for mod in rigContents:
            if '.pyc' not in mod or '.__init__' not in mod:
                self.rigModList.append(mod)
 
        # An empty list to store information collected from the UI.
        self.uiInfo = []
 
    def ui(self, *args):
        """Check to see if UI exists """
        windowName = "Window"
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)
        """ define width and height for buttons and windows"""
        windowWidth = 240
        windowHeight = 120
        buttonWidth = 55
        buttonHeight = 22
 
        self.UIElements["window"] = cmds.window(windowName, width=windowWidth, height=windowHeight, title="LBS_UI", sizeable=True)
 
        self.UIElements["mainColLayout"] = cmds.columnLayout(adjustableColumn=True)
        self.UIElements["guiiFrameLayout1"] = cmds.frameLayout( label='layout', p=self.UIElements["mainColLayout"])
        self.UIElements["guiiFlowLayout1"] = cmds.flowLayout(v=False, width=windowWidth, height=windowHeight/2, wr=True, bgc=[0.2, 0.2, 0.2], p=self.UIElements["guiiFrameLayout1"])
 
 
        # Dynamically make a button for each rigging module.
        for mod in self.rigModList:
            buttonName = mod.replace('.py', '')
            cmds.separator(w=10, hr=True, st='none', p=self.UIElements["guiiFlowLayout1"])
            self.UIElements[buttonName] = cmds.button(label=buttonName, width=buttonWidth,  height=buttonHeight, bgc=[0.2, 0.4, 0.2], p=self.UIElements["guiiFlowLayout1"], c=partial(self.rigMod, buttonName))
 
        """show the Window"""
        cmds.showWindow(windowName)
 
    def rigMod(self, modFile, *args):
        """__import__ basically opens a module and read some info from
        it without actually loading the module in memory."""
        mod = __import__('rig.' + modFile, {}, {}, [modFile])
 
        #python getattr will get an attribute from a class.
        moduleClass = getattr(mod, mod.className)
        moduleInstance = moduleClass()