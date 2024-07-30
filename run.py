import os
import shutil
import maya.cmds as cmds
import maya.mel as mel
import sys

def onMayaDroppedPythonFile(*args):
    installer_directory = os.path.dirname(__file__).replace('\\', '/')
    print("Arguments received:", installer_directory)
    sys.path.append(installer_directory)

