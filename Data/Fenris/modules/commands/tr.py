#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import * 

#
# Command
#
class TrCommand(Command):

	# Constructor
	def __init__(self):
		self.register('/tr', self.command)
		return
		
	# Comando move
	def command(self, player, arguments):
		if not player.is_admin():
			return False
		if len(arguments) == 1:
			index = Server.find_by_name(arguments[0])
			if (index >= 0):
				target = Player(index)
				target.teleport(player.get_map(), player.get_x(), player.get_y())
				target.message('[Sistema] Voce foi movido por %s' % player.get_name())
				player.message('[Sistema] Personagem movido.')
			else:
				player.message('[Sistema] O personagem esta offline ou nao existe.')
		else:
			player.message('Uso: /tr <nome>')
			return True
		return True

commands.register(TrCommand())