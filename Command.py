#!/usr/bin/python3
# -*- coding: utf-8 -*-

# C+R, S+R, A+R R A D G D E K
# RightClick, MiddleClick, LeftClick # RightClick x=123.4 y=333.3
# Enter Space backspace

from queue import Queue
import pyautogui

def alphaOnly(str):
	return str.count() == 1

def specialKey(str):
	return str.count() == 3

def pointSearch(str):
	xIdx = str.find('x')+2
	yIdx = str.find('y')+2
	x = ''
	y = ''
	while not str[xIdx] == ' ':
		x += str[xIdx]
		xIdx += 1
	while not str[yIdx] == '\0':
		y += str[yIdx]
		yIdx += 1
	
	return x, y

def commandsExe(commands):
	while not commands.empty():
		str = commands.get()
		
		if alphaOnly(str):
			pyautogui.press( str[0].lower() )
		
		elif specialKey(str):
			if str[0] == 'S':
				pyautogui.hotkey('shift',s[0].lower())
			elif str[0] == 'C':
				pyautogui.hotkey('ctrl',s[0].lower())
			elif str[0] == 'A':
				pyautogui.hotkey('alt',s[0].lower())
			
		elif 'Click' in str:
			x, y = pointSearch(str)
			pyautogui.moveTo(int(x), int(y))
			if 'right' in str:
				pass
			if 'middle' in str:
				pass
			if 'left' in str:
				pass
		
		elif 'Drag' in str:
			pass
		else:
			pyautogui.press(str.lower())
