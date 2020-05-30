import subprocess
import win32com.client
import os
from pathlib import Path
import pprint
import glob


print(os.environ['APPDATA'] + r'\Microsoft\Windows\Start Menu\Programs')
path = os.environ['ALLUSERSPROFILE'] + r'\Microsoft\Windows\Start Menu\Programs' 

p_temp = Path(path)

print(type(p_temp.glob('**/*.lnk')))
appName = 'p-study system 8'
list = list(p_temp.glob('**/*.lnk'))
for l in list:
	s = os.path.basename(l).replace('.lnk', '')
	print(s)
	if s.lower() in appName.lower():
		print(l)
		wshell = win32com.client.Dispatch("WScript.shell")
		shortcut = wshell.CreateShortcut(str(l))
		print(shortcut.TargetPath)
		subprocess.Popen(shortcut.TargetPath)

		#wshell = win32com.client.Dispatch("WScript.shell")
		#shortcut = wshell.CreateShortcut(path + '\\' + l)
		#print(shortcut.TargetPath)
		#subprocess.Popen(shortcut.TargetPath)