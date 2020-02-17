#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
import json
from queue import Queue
import os
import Command # Command.py


class JsonFiles:
	def __init__(self, output, appName, scriptName):
		self.output = output
		self.appName = appName + '/'
		self.scriptName = scriptName
		
		
	def write(self):
		self.scriptName += '.txt'
		path = self.appName
		
		if not os.path.exists(path):
			os.makedirs(path)
		
		with open(os.path.join(path, self.scriptName), mode='w', encoding='utf-8') as f:
			while not self.output.empty():
				f.write(self.output.get())
				f.write('\n')
		
		print('Write End')

	def read(self):
		print('UNKOY(')
		error = 0
		path = self.appName + self.scriptName
		print('! ' + path)
		command = Queue()
		with open(path) as f:
			s = f.read()
			print(s)
			command.put(s)
		
		error = Command.commandExe(command)
		return error

def main(output, scriptName, appName):
	scriptName = 'UNddddO'
	appName = 'KEIO'
	jsonFile = jsonFiles(output, scriptName, appName)