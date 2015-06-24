#!/usr/bin/python

from editorpy import Environment
from os import getcwd

env = Environment(getcwd())
env.prompt = ">>>"
print("env exited with code: " + str(env.run()))