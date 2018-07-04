import maya.cmds as cmds
import json
import tempfile

def writeJson(fileName, rig_data):
	with open(fileName, 'w') as outfile:
		json.dump(rig_data, outfile)
	file.close(outfile)

def readJson(fileName):
	with open(fileName, "r") as infile:
		rig_data = (open(infile.name, 'r').read())
	return rig_data