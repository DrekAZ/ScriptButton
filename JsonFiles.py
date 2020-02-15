#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
import json
from queue import Queue
import os
import Command # Command.py


class JsonFiles:
	def __init__(self, output=None, appName=None, scriptName=None):
		pass
	def write(self, output, appName, scriptName):
		scriptName = scriptName + '.txt'
		path = appName + '/'
		
		if not os.path.exists(path):
			os.makedirs(path)
		
		with open(os.path.join(path, scriptName), mode='w') as f:
			while not output.empty():
				f.write(output.get())
				f.write('\n')
		
		print('THANKL')

	def read(self, appName, scriptName):
		path = appName + '/' + scriptName
		command = Queue()
		print(path)
		with open(path, encoding='utf-8') as f:
			print(f)
			command.put(f)
		
		Command.commandExe(command)

def main(output, scriptName, appName):
	scriptName = 'UNddddO'
	appName = 'KEIO'
	jsonFile = jsonFiles(output, scriptName, appName)