#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
	QAction, QInputDialog, QTabWidget, QWidget, QVBoxLayout)
from PyQt5.QtGui import QIcon
from multiprocessing import Process, Queue

import Monitor ## Monitor.py
from JsonFiles import JsonFiles ## jsonFiles.py

output = Queue()

class GUI(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.signal = pyqtSignal()
		
		self.process = None
		self.scriptName = ''
		self.tabs = QTabWidget()
		self.menu = None
		
		self.initUI()
	
	def initUI(self):
		#button = QPushButton("マクロ 記録/停止", self)
		#button.move(100, 100)
		#button.clicked.connect(self.record)
		
		# icon
		recIcon = QAction(QIcon('rec.png'), 'REC', self)
		recIcon.setShortcut('Ctrl+R')
		recIcon.setCheckable(True)
		recIcon.toggled.connect(self.record)
		
		# toolbar
		self.toolbar = self.addToolBar('toolbar')
		self.toolbar.addAction(recIcon)
		
		# menubar
		menubar = self.menuBar()
		self.menu = menubar.addMenu('&メニュー')
		self.menu.addAction(recIcon)
		self.add()
		
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)
		tab1 = QWidget()
		self.tabs.addTab(tab1, 'New')
		self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
		self.setCentralWidget(self.tabs)
		
		# window
		self.setWindowTitle("Qt5")
		self.setGeometry(1100, 400, 480, 600)
		self.show()
	
	def record(self, checked):
		global process
		global output
		if checked:
			process = Process(target=Monitor.main, args=(output,))
			process.start()
		else:
			process.terminate()
			process.join()
			process.close()
			self.inputDialog()
			if self.scriptName != '':
				print ('START&')
				appName = ''
				while not output.empty():
					str = output.get()
					
					if 'appName' in str:
						idx = str.find('appName')+7
						for i in range(idx, len(str)):
							appName += str[idx]
							idx += 1
							
						break
					#print(output.get())
					print(appName)
				
				JsonFiles(output, appName, self.scriptName).write()
				self.add(self.menu)
		
	def inputDialog(self):
		scriptName, ok = QInputDialog.getText(self, 'Script Name', 'Enter script name:')
		if ok:
			self.scriptName = scriptName
			
	def add(self):
		path = os.getcwd()
		path = path + '/'
		for dir in os.listdir(path):
			if os.path.isdir(dir) and not ('__' in dir):
				print(dir)
				nowDir = dir
				appSelect = QAction(dir, self)
				#appSelect.setStatusTip(dir)
				appSelect.triggered.connect(lambda: self.click_appSelect(nowDir))
				self.menu.addAction(appSelect)
			
	def click_appSelect(self, dir):
		print(dir)
		tab = QWidget()
		tab.layout = QVBoxLayout()
		listFiles = os.listdir(dir)
		for i, file in enumerate(listFiles):
			if os.path.isfile(dir + '/' + file):
				print('e : ' + file)
				button = QPushButton(file)
				jsonFiles = JsonFiles(None, dir, file)
				button.clicked.connect(lambda: self.btnClick(dir, file))
				#tab.layout.addStretch(1)
				tab.layout.addWidget(button)
			
		tab.setLayout(tab.layout)
		self.tabs.addTab(tab, dir)
		#print(type(command))
		
	def btnClick(self, dir, file):
		jsonFiles = JsonFiles(None, dir, file)
		error = jsonFiles.read()
		if error == 1:
			QMessageBox.infomation(self, "Error", "Error : app can not find")
		
	

if __name__ == "__main__":
	app = QApplication(sys.argv)
	gui = GUI()
	sys.exit(app.exec_())