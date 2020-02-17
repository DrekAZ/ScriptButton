#!/usr/bin/python3
# -*- coding: utf-8 -*-

# C+R, S+R, A+R R A D G D E K
# RightClick, MiddleClick, LeftClick # RightClick x=123.4 y=333.3
# Enter Space backspace

from queue import Queue
import pyautogui
import win32gui
import subprocess
import os

def alphaOnly(str):
	print(len(str))
	return len(str) == 1

def specialKey(str):
	return len(str) == 3

def clickPoint(str):
	xIdx = str.find('x')+2
	yIdx = str.find('y')+2
	x = ''
	y = ''
	while not str[xIdx] == 'y':
		x += str[xIdx]
		xIdx += 1
	while not str[yIdx] == '\n':
		y += str[yIdx]
		yIdx += 1
	
	print(x +' '+ y)
	return int(x), int(y)

def dragPoint(str):
	fx = str.find('from_x')+2
	fy = str.find('from_y')+2
	tx = str.find('to_x')+2
	ty = str.find('to_y')+2
	frx = ''
	fry = ''
	tox = ''
	toy = ''
	while not str[fx] == 'f':
		frx += str[fx]
		fx += 1
	while not str[fy] == 't':
		fry += str[fy]
		fy += 1
	while not str[tx] == 't':
		tox += str[tx]
		tx += 1
	while not str[ty] == '\n':
		toy += str[ty]
		ty += 1
	
	return int(frx), int(fry), int(tox), int(toy)
	
def commandExe(commands):
	error = 0
	while not commands.empty():
		str = commands.get()
		print('command : ' + str)
		if alphaOnly(str):
			pyautogui.press( str[0].lower() )
		
		elif specialKey(str):
			if str[0] == 's':
				pyautogui.hotkey('shift',s[0].lower())
			elif str[0] == 'c':
				pyautogui.hotkey('ctrl',s[0].lower())
			elif str[0] == 'a':
				pyautogui.hotkey('alt',s[0].lower())
			
		elif 'Click' in str:
			x, y = clickPoint(str)
			pyautogui.moveTo(x, y)
			if 'left' in str:
				pyautogui.click(button='left')
			if 'middle' in str:
				pyautogui.click(button='middle')
			if 'right' in str:
				pyautogui.click(button='right')
				
		elif 'Double' in str:
			x, y = clickPoint(str)
			pyautogui.moveTo(x, y)
			if 'left' in str:
				pyautogui.click(clicks=2, interval=0.5, button='left')
			if 'middle' in str:
				pyautogui.click(clicks=2, interval=0.5, button='middle')
			if 'right' in str:
				pyautogui.click(clicks=2, interval=0.5, button='right')
				
		elif 'Drag' in str:
			frx, fry, tox, toy = dragPoint(str)
			pyautogui.moveTo(frx, fry)
			if 'left' in str:
				pyautogui.click(tox, toy, button='left')
			if 'middle' in str:
				pyautogui.click(tox, toy, button='middle')
			if 'right' in str:
				pyautogui.click(tox, toy, button='right')
				
		elif 'appName' in str:
			idx = str.find('appName')+7
			appName = ''
			while not idx == len(str):
				appName += str[idx]
				idx += 1
			
			num = win32gui.FindWindow(None, appName)
			if num != 0:
				win32gui.SetForegroundWindow(num)
			else:
				dirUser = os.listdir(os.environ['APPDATA'] + r'\Microsoft\Windows\Start Menu\Programs')
				dirSys = os.listdir(os.environ['ALLUSERSPROFILE'] + r'\Microsoft\Windows\Start Menu\Programs')
				finded = 0
				
				p_temp = Path(dirSys)
				list = list(p_temp.glob('**/*.lnk'))
				for l in list:
					s = os.path.basename(l).replace('.lnk', '')
					print(s)
					if s.lower() in appName.lower():
						wshell = win32com.client.Dispatch("WScript.shell")
						shortcut = wshell.CreateShortcut(str(l))
						subprocess.Popen(shortcut.TargetPath)
						finded = 1
						break
				
				if not finded:
					p_temp = Path(dirUser)
					list = list(p_temp.glob('**/*.lnk'))
					for l in list:
						s = os.path.basename(l).replace('.lnk', '')
						print(s)
						if s.lower() in appName.lower():
							wshell = win32com.client.Dispatch("WScript.shell")
							shortcut = wshell.CreateShortcut(str(l))
							subprocess.Popen(shortcut.TargetPath)
							finded = 1
							break
				
				if not finded:
					error = 1
				
		else: # space backspace enter
			pyautogui.press(str.lower())
			
	return error
		
