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

def clickPoint(str):
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
	while not str[fx] == ' ':
		frx += str[fx]
		fx += 1
	while not str[fy] == ' ':
		fry += str[fy]
		fy += 1
	while not str[tx] == ' ':
		tox += str[tx]
		tx += 1
	while not str[ty] == ' ':
		toy += str[ty]
		ty += 1
	
	return int(frx), int(fry), int(tox), int(toy)
def commandsExe(commands):
	while not commands.empty():
		str = commands.get()
		print(str)
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
				
		else:
			pyautogui.press(str.lower())
