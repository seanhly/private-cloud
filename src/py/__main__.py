#!/usr/bin/python3
from user_actions import UserAction
from parse_dynamic_argument import parse_dynamic_argument
from typing import Type
import sys

action = sys.argv[1]
args = sys.argv[2:]
arguments = [
	parse_dynamic_argument(arg, action)
	for arg in args
]


def find_action(parent_class: Type[UserAction]):
	for T in parent_class.__subclasses__():
		if action == T.command():
			return T
		else:
			found_action = find_action(T)
			if found_action:
				return found_action
	return None


FoundAction = find_action(UserAction)
if FoundAction:
	FoundAction(arguments).start()
	exit_code = 0
else:
	sys.stderr.write(f"unknown sub-command: {action}\n")
	exit_code = 1
sys.exit(exit_code)
