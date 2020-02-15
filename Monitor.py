#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pynput import mouse, keyboard
from multiprocessing import Queue
import win32gui
import re
import time

altTabFunc = 'タスクの切り替え'

class Monitor:
	def __init__(self, output):
		self.counter = 0
		self.over_count = 3
		self.output = output
		self.appName = ''
		self.from_x = 0
		self.from_y = 0
		self.specialKey = None
		self.pressed = 0
		self.first_time = 0
	
	def count(self):
		self.counter += 1
		print('Count:{0}'.format(self.counter))
	
	def is_over(self):
		return True if self.counter >= self.over_count else False
	
	def call(self):
		self.count()
		if self.is_over():
			print('Done')
			self.stop()
	
	# マウス入力
	def on_click(self, x, y, button, pressed):
		print('{0}{1} at {2}'.format('Pressed' if pressed else 'Released',button,(x,y)))
		self.getAppName()
		print(str(button))
		if pressed:
			self.from_x = x
			self.from_y = y
			self.call()
			if self.first_time == 0:
				self.first_time = time.perf_counter()
			else:
				t = time.perf_counter() - self.first_time
				self.first_time = 0
				print('t : : : ' + str(t))
				if t <= 0.5:
					self.output.put(btn.group() + 'Double' + 'x=' + str(x) + 'y=' + str(y))
		if not pressed:
			btn = re.search(r'(left)|(right)|(middle)', str(button))
			print(btn.group())
			if btn:
				if self.from_x != x or self.from_y != y:
					print('DRAG')
					self.output.put(btn.group() + 'Drag ' + 'from_x=' + str(self.from_x) + 'from_y' + str(self.from_y)
																				+ 'to_x=' + str(x) + 'to_y=' + str(y))
				else:
					self.output.put(btn.group() + 'Click ' + 'x=' + str(x) + 'y=' + str(y))
	
	# キーボード入力
	def on_press(self, key):
		self.getAppName()
		#self.output.put(key)
		try:
			print('alphanumeric key {0} pressed'.format(key.char))
			if self.specialKey:
				self.pressed = 1
		
		except AttributeError:
			print('special key {0} pressed'.format(key))
			print(str(key))
			spkey = re.search(r'(shift)|(alt)|(ctrl)|(space)|(enter)|(backspace)|(tab)|(cmd)|(up)|(left)|(down)|(right)|(esc)|(home)|(end)|(insert)|(delete)|(f.)', str(key)) # ctrl a \x11
			self.specialKey = spkey.group()
			print(spkey)
			print('SPECIAL :'+self.specialKey)
			#self.output.put(key)
		
		
	
	def on_release(self, key):
		try:
			print('alphanumeric key {0} released'.format(key.char))
			if self.specialKey == 'ctrl':
				k = re.search('[0-9][0-9]', str(key))
				k = str(r'0x' + k.group())
				k = int(k, 0)
				if k>=1 and k<=26:
					k = chr( k + 64)
					print(k)
					print('ctrl + ?')
					self.output.put(self.specialKey[0] + '+' + k.lower())
			elif self.specialKey:
				print('special ? + ?' + self.specialKey[0])
				self.output.put(self.specialKey[0] + '+' + key.char)
			else:
				print('PUT : only ' + key.char)
				self.output.put(key.char)
				
			#self.pressed = 0
		except AttributeError:
			print('special key {0} released'.format(key))
			
			if self.specialKey and self.pressed == 0:
				print('RE SP : ' + self.specialKey)
				self.output.put(self.specialKey)
			else:
				print('sp : only ')
				#self.output.put(self.specialKey)
				
				
			self.specialKey = None
			self.pressed = 0
			#if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
				#self.getAppName()
	
	def start(self):
		with mouse.Listener(
			on_click=self.on_click) as self.mouse_listener, keyboard.Listener(
			on_press=self.on_press, on_release=self.on_release) as self.keyboard_listener:
			self.mouse_listener.join()
			self.keyboard_listener.join()
	
	def stop(self):
		self.mouse_listener.stop()
		self.keyboard_listener.stop()
		#return out
	
	def getAppName(self):
		global altTabFunc
		app = win32gui.GetWindowText(win32gui.GetForegroundWindow())
		if self.appName == '':
			self.appName = app
			print('First: ' + self.appName)
		elif not self.appName == app:
			self.appName = app
			print('SECOND : '+self.appName)
			self.output.put(self.appName)

def main(output):
	monitor = Monitor(output) # output
	monitor.start()
	
if __name__ == "__main__":
	monitor = Monitor(Queue())
	monitor.start()
	#parent_handle = win32gui.FindWindow(None, "Discord")
	#print(parent_handle)
	#win32gui.SetForegroundWindow(parent_handle)
	