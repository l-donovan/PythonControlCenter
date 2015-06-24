#!/usr/bin/python
from __future__ import print_function

from sys import exit
from os import listdir
from os.path import isfile, join
from utils import *

class Environment():
	def checkFiles(self):
		return [ f for f in listdir(self.dir) if isfile(join(self.dir, f)) ]

	def runCommand(self, command):
		# Return format: [printResult, commandResult, systemFlag]
		baseCommand = command.split()[0]
		args = command.split()[1:]
		if baseCommand == "exit":
			return [None, None, "exit, " + args[0]]
		elif baseCommand == "print":
			return [" ".join(args), None, None]
		elif baseCommand == "testResult":
			return [None, " ".join(args), None]
		elif baseCommand == "termInfo":
			output = "Window size: " + str(getTerminalSize()[0]) + " * " + str(getTerminalSize()[1])
			return [output, None, None]
		elif baseCommand == "clear":
			print(clear())
			return [clear(), None, None]
		else:
			return [None, "Command not recognized", None]

	def __init__(self, cd):
		self.dir = cd
		(self.width, self.height) = getTerminalSize()
		self.stringIn, self.stringInPrev, self.commandResultPrev = "", "", ""
		self.prompt = ">"
		self.commandPrefix = "* "
		self.commandResult = self.commandPrefix
		self.paths = self.checkFiles()
		self.results = fuzzyfinder("", self.paths)
		self.temp_results = (str(self.results)[:self.width - 3] + '...') if len(str(self.results)) > (self.width - 3) else str(self.results)

	def run(self):
		print(self.commandPrefix + '\n' + self.prompt + '\n' + self.temp_results + moveUp(2))
		while True:
			self.charIn = getch()
			stringInPrev = self.stringIn
			self.resultsPrev = self.results
			self.commandResultPrev = self.commandResult

			if self.charIn == '\x03' or self.charIn == '\x1A': 
				print(clear() + "Please exit with the '/exit' command\n")
			elif self.charIn == '\x7F' or self.charIn == '\x08': # x7f is technically delete, but lots of systems use it as backspace
				self.stringIn = self.stringIn[:-1]
			elif self.charIn == "\t":
				self.stringIn = self.results[0]
			elif self.charIn == "\r":
				print(clear())
				if self.stringIn != "":
					if self.stringIn[0] == "/":
						self.output = self.runCommand(self.stringIn[1:])
						if self.output[2] and self.output[2].split(',')[0].strip() == "exit": 
							return(int(self.output[2].split(',')[1].strip()))
						if self.output[0]: 
							print(self.output[0] + '\n')
						self.commandResult = self.commandPrefix + self.output[1] if self.output[1] else self.commandPrefix
					else:
						try:
							self.readFile = open(self.results[0])
							print(self.commandPrefix + "Begin \"" + self.results[0] + "\"")
							print(self.readFile.read())
							self.commandResult = self.commandPrefix + "End \"" + self.results[0] + "\""
						except IndexError:
							self.commandResult = self.commandPrefix + "File not found"
					self.stringIn = ""
				else:
					self.commandResult = self.commandPrefix
			else:
				self.stringIn += self.charIn

			self.results = fuzzyfinder(self.stringIn, self.paths)
			self.commandResultLine = (self.commandResult[:self.width - 3] + '...') if len(self.commandResult) > (self.width - 3) else self.commandResult
			self.stringInLine = (self.stringIn[:self.width - 3 - len(self.prompt)] + '...') if len(self.stringIn) > (self.width - 3 - len(self.prompt)) else self.stringIn
			self.resultsLine = (str(self.results)[:self.width - 3] + '...') if len(str(self.results)) > (self.width - 3) else str(self.results)

			print(moveUp(1) + moveLeft(self.width) + \
				clearLine() + self.commandResultLine + '\n' + \
				clearLine() + self.prompt + self.stringInLine + '\n' + \
				clearLine() + self.resultsLine + \
				moveUp(1), end='\r')
			print(moveRight(len(self.stringIn) + len(self.prompt)), end='')

	def refresh(self):
		self.__init__(self.dir)