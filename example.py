#!/usr/bin/python

from editor import Environment
from os import getcwd

env = Environment(getcwd())
env.prompt = "Pointlessly Long Prompt!>"
print(env.run())