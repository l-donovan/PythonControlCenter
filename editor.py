#!/usr/bin/python
from __future__ import print_function

from sys import exit
from utils import *
from os import getcwd, listdir
from os.path import isfile, join

def runCommand(command):
	baseCommand = command.split()[0]
	args = command.split()[1:]
	if baseCommand == "quit":
		exit(0)
	elif baseCommand == "print":
		return [" ".join(args), ""]
	elif baseCommand == "testResult":
		return [None, " ".join(args)]
	else:
		return [None, "Command not recognized"]

def checkFiles():
	return [ f for f in listdir(getcwd()) if isfile(join(getcwd(), f)) ]

def mainLoop():
	(width, height) = getTerminalSize()
	stringIn, stringInPrev, commandResultPrev = "", "", ""
	prompt = ">"
	commandPrefix = "* "
	commandResult = commandPrefix
	paths = checkFiles()
	results = fuzzyfinder("", paths)
	temp_results = (str(results)[:width - 3] + '...') if len(str(results)) > (width - 3) else str(results)
	print(commandPrefix + '\n' + prompt + '\n' + temp_results + moveUp(2))
	while True:
		charIn = getch()
		stringInPrev = stringIn
		resultsPrev = results
		commandResultPrev = commandResult

		if charIn == '\x03' or charIn == '\x1A': 
			print(clear() + "Please exit with the '/quit' command\n")
		elif charIn == '\x7F' or charIn == '\x08': # x7f is technically delete, but lots of systems use it as backspace
			stringIn = stringIn[:-1]
		elif charIn == "\t":
			stringIn = results[0]
		elif charIn == "\r":
			print(clear())
			if stringIn != "":
				if stringIn[0] == "/":
					output = runCommand(stringIn[1:])
					if output[0]: print(output[0] + '\n')
					commandResult = commandPrefix + output[1]
				else:
					try:
						readFile = open(results[0])
						print(commandPrefix + "Begin \"" + results[0] + "\"")
						print(readFile.read())
						commandResult = commandPrefix + "End \"" + results[0] + "\""
					except IndexError:
						commandResult = commandPrefix + "File not found"
				stringIn = ""
			else:
				commandResult = commandPrefix
		else:
			stringIn += charIn

		results = fuzzyfinder(stringIn, paths)
		commandResultLine = (commandResult[:width - 3] + '...') if len(commandResult) > (width - 3) else commandResult
		stringInLine = (stringIn[:width - 3 - len(prompt)] + '...') if len(stringIn) > (width - 3 - len(prompt)) else stringIn
		resultsLine = (str(results)[:width - 3] + '...') if len(str(results)) > (width - 3) else str(results)

		print(moveUp(1) + moveLeft(width) + \
			clearLine() + commandResultLine + '\n' + \
			clearLine() + prompt + stringInLine + '\n' + \
			clearLine() + resultsLine + \
			moveUp(1), end='\r')
		print(moveRight(len(stringIn) + 1), end='')

mainLoop()