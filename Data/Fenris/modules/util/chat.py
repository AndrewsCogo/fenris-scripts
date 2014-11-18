#
# Imports
#
from wolfulus import *
from player import *

#
# Handler class
#
class ChatHandler(object):

	# Constructor
	def __init__(self):
		self.handlers = []
		Events.register('player.message', self.chat)
		return
		
	# Register a command
	def register(self, handler):
		self.handlers.append(handler)
		return
		 
	# Process the incoming text into commands
	def process(self, player, command):
		command = command.split(' ')
		arguments = command[1:]
		command = command[0].lower()
		for handler in self.handlers:
			if handler.execute(player, command, arguments):
				return True
		return False
		
	#
	# Chat handler
	#
	def chat(self, index, text):
		player = Player(index)
		if text.startswith('$'):
			if player.is_admin():
				Server.send_announcement_all('[%s]' % player.get_name())
				Server.send_announcement_all(text[1:])
			return True

		return self.process(player, text)
#
# Command class
#		
class Command(object):

	# Variables
	dispatchers = dict()
	
	# Constructor
	def __init__(self):	
		pass
		
	# Registers a new dispatcher to this command
	def register(self, prefix, dispatcher):
		self.dispatchers[prefix.lower()] = dispatcher
		Console.write('> %s' % prefix.lower())
		return
		
	# Executes a dispatcher
	def execute(self, player, command, arguments):
		command = command.lower()
		if not command in self.dispatchers:
			return False
		dispatcher = self.dispatchers[command]
		return dispatcher(player, arguments)

#
# Command handler instance
#
commands = ChatHandler()