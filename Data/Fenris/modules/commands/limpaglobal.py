#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import * 

#
# Command
#
class LimpaGlobalCommand(Command):
	
	# Constructor
	def __init__(self):
		self.register('/limparglobal', self.command_limpar)
		return
		
	# Comando de limpar global
	def command_limpar(self, player, arguments):
		if not player.is_admin():
			return True
		Server.send_announcement_all('')
		Server.send_announcement_all('')
		Server.send_announcement_all('')
		Server.send_announcement_all('')
		Server.send_announcement_all('')
		Server.send_announcement_all('')
		player.message('[Sistema] O Global foi limpo!')
		return True

#
# Initialization
#
commands.register(LimpaGlobalCommand())