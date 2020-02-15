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
		menu = menubar.addMenu('&メニュー')
		menu.addAction(recIcon)
		self.add(menu)
		
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
				while not output.empty():
					print(output.get())
				
				#JsonFiles(output, appName, self.scriptName).write()
		
	def inputDialog(self):
		scriptName, ok = QInputDialog.getText(self, 'Script Name', 'Enter script name:')
		if ok:
			self.scriptName = scriptName
			
	def add(self, menu):
		path = os.getcwd()
		path = path + '/'
		for dir in os.listdir(path):
			if os.path.isdir(dir) and not ('__' in dir):
				print(dir)
				nowDir = dir
				appSelect = QAction(dir, self)
				#appSelect.setStatusTip(dir)
				appSelect.triggered.connect(lambda: self.click_appSelect(nowDir))
				menu.addAction(appSelect)
			
	def click_appSelect(self, dir):
		print(dir)
		tab = QWidget()
		tab.layout = QVBoxLayout()
		listFiles = os.listdir(dir)
		for i, file in enumerate(listFiles):
			if os.path.isfile(dir + '/' + file):
				print(file)
				button = QPushButton(file, self)
				button.clicked.connect(JsonFiles(None, dir, file).read)
				#tab.layout.addStretch(1)
				tab.layout.addWidget(button)
			
		tab.setLayout(tab.layout)
		self.tabs.addTab(tab, dir)
		print(type(command))
		
		

if __name__ == "__main__":
	app = QApplication(sys.argv)
	gui = GUI()
	sys.exit(app.exec_())