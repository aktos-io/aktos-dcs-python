# use this if you want to include modules from a subfolder
import os
import sys
import inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
 sys.path.insert(0, cmd_subfolder)

aktos_dcs_lib_folder = os.path.realpath(os.path.abspath(os.path.join(cmd_subfolder, "..", "aktos-dcs-lib")))

if aktos_dcs_lib_folder not in sys.path:
 sys.path.insert(0, aktos_dcs_lib_folder)
