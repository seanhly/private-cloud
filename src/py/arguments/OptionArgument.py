from arguments.Argument import Argument
import re
from typing import cast

from arguments.IPArgument import IPArgument


class OptionArgument(Argument):
	option: str

	def __init__(self, option: str, _=None):
		# Trim off the leading double-hyphen.
		self.option = option[2:]

	def __str__(self):
		return self.option

	def parse_argument_for_action(self, arguments, current_index, action):
		from user_actions.UserAction import UserAction
		the_action: UserAction = action
		current_index += 1
		if self.option in the_action.disqualified_options:
			the_action.conflicting_options[self.option] = (
				the_action.indexed_blocking_options()[self.option]
			)
		if self.option not in the_action.recognised_options():
			the_action.unrecognised_options.add(self.option)
		else:
			the_action.options[self.option] = None
			if self.option in the_action.indexed_obligatory_option_groups():
				for o in the_action.indexed_obligatory_option_groups()[self.option]:
					del the_action.indexed_obligatory_option_groups()[o]
			if self.option in the_action.indexed_blocking_options():
				for o in the_action.indexed_blocking_options()[self.option]:
					the_action.disqualified_options[o] = self.option
			if self.option in the_action.arg_options():
				if current_index >= len(arguments):
					the_action.missing_argument_for_options.append(self.option)
				else:
					argument = arguments[current_index]
					from arguments.OtherArgument import OtherArgument
					if type(argument) == type(self):
						the_action.missing_argument_for_options.append(self.option)
					else:
						for t in {OtherArgument, IPArgument}:
							if type(argument) == t:
								the_action.options[self.option] = (
									str(cast(t, argument))
								)
								current_index += 1
								break

		return current_index
			
	@classmethod
	def fits(cls, s: str) -> bool:
		return bool(re.fullmatch("--.*", s))
