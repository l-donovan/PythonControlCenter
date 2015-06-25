#!/usr/bin/python
from __future__ import print_function

from os import listdir
from os.path import isfile, join
from sys import exit
from utils import *
from re import compile

class Environment:
	def getFiles(self):
		return [ f for f in listdir(self.dir) if isfile(join(self.dir, f)) ]

	def refresh(self):
		self.paths = self.getFiles()
		self.results = fuzzyfinder(self.stringIn, self.paths)

	def printOut(self, output, commandResult, stringIn, results):
		if not output: output = ""
		if not commandResult: commandResult = ""
		if not stringIn: stringIn = ""
		self.commandResultLine = (commandResult[:self.width - 3] + '...') if len(commandResult) > (self.width - 3) else commandResult
		self.stringInLine = (stringIn[:self.width - 3 - len(self.prompt)] + '...') if len(stringIn) > (self.width - 3 - len(self.prompt)) else stringIn
		self.resultsLine = (str(results)[:self.width - 3] + '...') if len(str(results)) > (self.width - 3) else str(results)

		print(output)
		print(moveUp(1) + '\n' + moveLeft(self.width) + \
			clearLine() + self.commandResultPrefix + self.commandResultLine + '\n' + \
			clearLine() + self.prompt + self.stringInLine + '\n' + \
			clearLine() + self.resultsLine + \
			moveUp(1), end='\r')
		print(moveRight(len(self.stringIn) + len(self.prompt)), end='')

	def runCommand(self, command):
		# Format: [output, commandResult, systemFlag]
		baseCommand = command.split()[0]
		args = command.split()[1:]

		if baseCommand == "exit":
			try:
				return [None, None, "exit," + args[0]]
			except IndexError:
				return [None, None, "exit,0"]
		elif baseCommand == "print":
			return [" ".join(args), u'\u2713', None]
		elif baseCommand == "clear":
			return [clear(), u'\u2713', None]
		elif baseCommand == "termInfo":
			text = "Window size: " + str(getTerminalSize()[0]) + " * " + str(getTerminalSize()[1])
			text += "\n Safety buffer size: " + str(self.safety)
			return [text, u'\u2713', None]
		elif baseCommand == "testResult":
			return [None, " ".join(args[0:]), None]
		elif baseCommand == "set":
			self.vars[args[0]] = " ".join(args[1:])
			return [None, u'\u2713', None]
		elif baseCommand == "vars":
			for i in self.vars:
				print("{'%s': '%s'}" % (i, self.vars[i]))
			return [None, u'\u2713', None]
		elif baseCommand == "do":
			for i in range(0, int(args[0])):
				output = self.runCommand(" ".join(args[1:]))
				self.printOut(output[0], output[1], " ".join(args[1:]), "")
				print(moveLeft(len(command) + 1))
			return [None, u'\u2713', None]
		else:
			return [None, u"\u2717 Command not Found", None]


	def __init__(self, cd):
		self.dir = cd
		(self.width, self.height) = getTerminalSize()
		self.stringIn = ""
		self.charIn = ''
		self.stringInHist = []
		self.prompt = ">"
		self.commandResultPrefix = "* "
		self.commandResult = ""
		self.tabCompleteIndex = -1
		self.output = ""
		self.shouldPrint = True
		self.vars = {}
		self.safety = -1

	def run(self):
		self.refresh()
		self.printOut(self.output, self.commandResult, self.stringIn, self.results)
		while True:
			#self.results = fuzzyfinder(self.stringIn, self.paths)
			try:
				self.results = fuzzyfinder(self.stringIn, self.paths)
			except:
				self.results = fuzzyfinder(self.stringIn[:self.safety], self.paths)
				self.safety -= 1
			self.charIn = getch()
			print("|||\n\n\n" + self.charIn + "\n\n\n|||")
			if self.charIn == '\x03' or self.charIn == '\x1A': 
				self.commandResult = u"\u2717 Please exit with the '/exit' command"
			elif self.charIn == '\x7F' or self.charIn == '\x08':
				self.stringIn = self.stringIn[:-1]
			elif self.charIn == '\t':
				if self.tabCompleteIndex < len(self.results) - 1: 
					self.tabCompleteIndex += 1
				else:
					self.tabCompleteIndex = 0
				self.stringIn = self.results[self.tabCompleteIndex]
			elif self.charIn == '\x1b[A':
				break
			elif self.charIn == '\r':
				self.tabCompleteIndex = -1
				print(clear(), end='\r')
				if self.stringIn != "":
					if self.stringIn[0] == '/':
						commandOut = self.runCommand(self.stringIn[1:])
						if commandOut[2] and commandOut[2].split(',')[0].strip() == "exit": 
							return int(commandOut[2].split(',')[1].strip()) #commandOut[2] are system flags
						self.printOut(commandOut[0], commandOut[1], "", fuzzyfinder("", self.paths))
						print(moveLeft(len(self.stringIn)), end='')
						self.shouldPrint = False
					else:
						try:
							self.readFile = open(self.results[0])
							self.output = "Begin \"" + self.results[0] + "\"\n"
							self.output += self.readFile.read()
							self.readFile.close()
							self.commandResult = u"\u2713 End \"" + self.results[0] + "\""
							self.results = fuzzyfinder("", self.paths)
						except IndexError:
							self.commandResult = u"\u2717 File not found"
					self.stringIn = ""
				else:
					self.output = ""
					self.commandResult = ""
				self.safety = -1
			else:
				self.stringIn += self.charIn
			if self.shouldPrint:
				print(clear())
				self.printOut(self.output, self.commandResult, self.stringIn, self.results)
			self.shouldPrint = True
