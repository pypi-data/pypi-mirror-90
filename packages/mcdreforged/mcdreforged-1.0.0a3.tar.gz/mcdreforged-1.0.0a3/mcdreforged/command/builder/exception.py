class CommandErrorBase(Exception):
	pass


class IllegalNodeOperation(CommandErrorBase):
	"""
	This node is not allowed to do this
	"""
	pass


class CommandError(CommandErrorBase):
	"""
	The basic error, for errors raising when a command source is executing a command
	"""
	def __init__(self, message, parsed_command, failed_command):
		self.__message = message
		self._parsed_command = parsed_command
		self._failed_command = failed_command
		self.__handled = False

	def __str__(self):
		return '{}: {}<--'.format(self.__message, self._failed_command)

	def to_mc_color_text(self):
		return '§c{}: §r{}§c{}§4<--'.format(self.__message, self._parsed_command, self._failed_command[len(self._parsed_command):])

	def get_parsed_command(self):
		return self._parsed_command

	def get_failed_command(self):
		return self._failed_command

	def set_handled(self, value=True):
		"""
		It won't make any difference to the command node tree execution
		But it might be useful for outer error handlers
		"""
		self.__handled = value

	def is_handled(self):
		return self.__handled


class UnknownCommand(CommandError):
	"""
	When the command finishes parsing, but current node doesn't have a callback function
	"""
	def __init__(self, parsed_command, failed_command):
		super().__init__('Unknown Command', parsed_command, failed_command)


class UnknownArgument(CommandError):
	"""
	When there's remaining command string, but there's no matched Literal nodes and no general argument nodes
	"""
	def __init__(self, parsed_command, failed_command):
		super().__init__('Unknown Argument', parsed_command, failed_command)


class UnknownRootArgument(UnknownArgument):
	"""
	The same as UnknownArgument, but it fails to match at root node
	"""
	pass


class RequirementNotMet(CommandError):
	"""
	The specified requirement for the command source to enter this node is not met
	"""
	def __init__(self, parsed_command, failed_command):
		super().__init__('Permission denied', parsed_command, failed_command)

# -----------------
#   Syntax things
# -----------------


class CommandSyntaxError(CommandError):
	"""
	General illegal argument error
	Used in integer parsing failure etc.
	"""
	def __init__(self, message, char_read):
		super().__init__(message, '?', '?')
		self.message = message
		self.char_read = char_read

	def set_parsed_command(self, parsed_command):
		self._parsed_command = parsed_command

	def set_failed_command(self, failed_command):
		self._failed_command = failed_command


class IllegalArgument(CommandSyntaxError):
	"""
	General illegal argument error
	Used in integer parsing failure etc.
	"""
	pass


class LiteralNotMatch(CommandSyntaxError):
	"""
	Used by Literal node parsing failure for fail-soft
	"""
	pass


class NumberOutOfRange(CommandSyntaxError):
	"""
	The parsed number value is out of the restriction range
	"""
	pass


class EmptyText(CommandSyntaxError):
	"""
	The text is empty, and it's not allowed to be
	"""
	pass
