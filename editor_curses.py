#!/usr/bin/python
# editor_curses.py

from __future__ import print_function

import curses
from os import listdir, getcwd
from os.path import isfile, join
from sys import exit
from utils import fuzzyfinder

command = ""
commandHistory = ["", "aasdf", "qwieohrpoq", "xcv"]
historyIndex = 0
files = [ f for f in listdir(getcwd()) if isfile(join(getcwd(), f)) ]
results = fuzzyfinder(command, files)

screen = curses.initscr()
size = screen.getmaxyx()

BACKSPACE = curses.erasechar()
curses.noecho()
screen.keypad(True)
screen.border()
screen.hline(size[0] - 4, 1, '_', size[1] - 2)
screen.move(size[0] - 2, 1)
screen.addstr(\
	(str(results)[:size[1] - 5] + '...') if len(str(results)) > (size[1] - 5) else str(results))
screen.move(size[0] - 3, 1)
screen.addch('>')

def runCommand(command):
		baseCommand = command.split()[0]

		args = command.split()[1:]

		if baseCommand == "exit":
			try:
				exit(int(args[0]))
			except IndexError:
				exit(0)
		elif baseCommand == "print":
			return " ".join(args)
		elif baseCommand == "clear":
			writeOutput("", 0, 0)
			return ""
		elif baseCommand == "termInfo":
			text = "Window size:\n\t" + str(size[0]) + "(y) * " + str(size[1]) + "(x)"
			return text
		else:
			return "Command not found!"

def clearLine(fromBottom, fromLeft):
	screen.move(size[0] - 1 - fromBottom, fromLeft)
	screen.clrtoeol()
	screen.insch(size[0] - 1 - fromBottom, size[1] - 1, "|")
	screen.move(size[0] - 1 - fromBottom, fromLeft)

def redrawFuzzy(data):
	clearLine(1, 1)
	screen.addstr(\
		(str(data)[:size[1] - 5] + '...') if len(str(data)) > (size[1] - 5) else str(data))
	screen.move(pos[0], pos[1])

def writeOutput(data, fromTop, fromLeft):
	lines = data.split('\n')
	for index, line in enumerate(lines):
		screen.move(fromTop + 1 + index, fromLeft + 1)
		clearLine(size[0] - 2 - fromTop, 1)
		screen.addstr(\
		line[:size[1] - 5] + '...' if len(line) > (size[1] - 5) else line)
	screen.move(size[0] - 3, 2)

pos = [1, 1]
while True:
	char = screen.getch()

	if char == curses.KEY_LEFT:
		if pos[1] > 1:
			screen.move(pos[0], pos[1] - 1)
	elif char == curses.KEY_RIGHT:
		if pos[1] < size[1] - 2:
			screen.move(pos[0], pos[1] + 1)
	elif char == curses.KEY_UP:
		if historyIndex < len(commandHistory) - 1:
			historyIndex += 1
		else:
			historyIndex = 0
		clearLine(2, 2)
		screen.addstr(commandHistory[historyIndex])
		command = commandHistory[historyIndex]
	elif char == curses.KEY_DOWN:
		if historyIndex > 0:
			historyIndex -= 1
		else:
			historyIndex = len(commandHistory) - 1
		clearLine(2, 2)
		screen.addstr(commandHistory[historyIndex])
		command = commandHistory[historyIndex]
	elif char == 127:
		if pos[1] > 2:
			command = command[:-1]
			screen.move(size[0] - 3, 2)
			screen.clrtoeol()
			screen.addstr(command if len(command) <= size[1] - 4 else command[:size[1] - 7] + "...")
			screen.insch(size[0] - 3, size[1] - 1, "|")
			screen.move(size[0] - 3, 2 + (len(command) if len(command) < size[1] - 4 else size[1] - 4))
	elif char == 10:
		if command != "": 
			commandHistory.insert(0, command)
			clearLine(2, 2)
			if command[0] == '/':
				output = runCommand(command[1:])
				writeOutput(output, 0, 0)
		command = ""
		historyIndex = 0
	else:
		command += chr(char)
		if len(command) <= size[1] - 4: 
			screen.addch(char)
		else: 
			screen.move(pos[0], pos[1] - 3)
			screen.addstr("...")
	pos = screen.getyx()
	results = fuzzyfinder(command, files)
	redrawFuzzy(results)