#!/usr/bin/python

class _Getch:
	"""Gets a single character from standard input. Does not echo to the screen."""
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self): return self.impl()


class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()


getch = _Getch()

def moveUp(num):
	return chr(27) + '[' + str(num) + 'A'

def moveDown(num):
	return chr(27) + '[' + str(num) + 'B'

def moveRight(num):
	return chr(27) + '[' + str(num) + 'C'

def moveLeft(num):
	return chr(27) + '[' + str(num) + 'D'

def clear():
	return chr(27) + '[2J'