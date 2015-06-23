#!/usr/bin/python
from __future__ import print_function

from sys import exit
from utils import getch, moveUp, moveDown, moveRight, moveLeft, clear
from os import getcwd, listdir
from os.path import isfile, join

import re
def fuzzyfinder(user_input, collection):
	suggestions = []
	pattern = '.*?'.join(user_input)
	regex = re.compile('%s' % pattern)
	for item in collection:
		match = regex.search(item)
		if match:
			suggestions.append((len(match.group()), match.start(), item))
	return [x for _, _, x in sorted(suggestions)]

def runCommand(command):
	baseCommand = command.split()[0]
	args = command.split()[1:]
	if baseCommand == "quit":
		exit(0)
	elif baseCommand == "print":
		return [" ".join(args), ""]
	else:
		return [None, "Command not recognized"]

def checkFiles():
	return [ f for f in listdir(getcwd()) if isfile(join(getcwd(), f)) ]

def mainLoop():
	stringIn, stringInPrev, commandResultPrev = "", "", ""
	prompt = ">"
	commandPrefix = "* "
	commandResult = commandPrefix
	paths = checkFiles()
	results = fuzzyfinder("", paths)
	resultsPrev = results
	print(commandPrefix + '\n' + prompt + '\n' + str(fuzzyfinder("", paths)) + moveUp(2))
	while True:
		charIn = getch()
		stringInPrev = stringIn
		resultsPrev = results
		commandResultPrev = commandResult

		if charIn == '\x03' or charIn == '\x1A': 
			print("Please exit with the '/quit' command\n")
		elif charIn == "": # There is a backspace character in here
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
						commandResult = commandPrefix + "No file selected!"
				stringIn = ""
			else:
				commandResult = commandPrefix
		else:
			stringIn += charIn

		results = fuzzyfinder(stringIn, paths)
		commandResultLine = "".join(" " * len(commandResultPrev)) + "\r" + commandResult
		stringInLine = "".join(" " * len(stringInPrev)) + "\r" + prompt + stringIn
		resultsLine = "".join(" " * len(str(resultsPrev))) + "\r" + str(results)

		print(moveUp(1) + \
			commandResultLine + '\n' + \
			prompt + stringInLine + '\n' + \
			resultsLine + \
			moveUp(1), end='\r')

mainLoop()