#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import *

#
# Command
#
class DisconnectCommand(Command):
	
	# Constructor
	def __init__(self):
		self.register('/dc', self.command)
		self.register('/disconnect', self.command)
		return
	
	#	
	# Comando dc
	#
	def command(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 1:
			player.message('Uso: /dc <nome>')
			return True
		index = Server.find_by_name(arguments[0])
		if (index >= 0):
			target = Player(index)
			Server.send_announcement_all('[Sistema]');
			Server.send_announcement_all('%s desconectou %s' % (player.get_name(), target.get_name()));
			target.disconnect()
		else:
			player.message('[Sistema] O char informado nao existe ou nao esta online.')
		return True

#
# Initialization
#
commands.register(DisconnectCommand())
