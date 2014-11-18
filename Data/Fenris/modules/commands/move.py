#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import * 

#
# Command
#
class MoveCommand(Command):

	# Constructor
	def __init__(self):
		self.register('/move', self.command)
		return
		
	# Comando move
	def command(self, player, arguments):
		if not player.is_admin():
			return False
		if len(arguments) == 1:
			index = Server.find_by_name(arguments[0])
			if (index >= 0):
				target = Player(index)
				target.teleport(0, 125, 125)
				target.message('[Sistema] Voce foi movido por %s' % player.get_name())
				player.message('[Sistema] Personagem movido.')
			else:
				player.message('[Sistema] O personagem esta offline ou nao existe.')
		elif len(arguments) == 4:
			index = Server.find_by_name(arguments[0])
			if (index >= 0):
				target = Player(index)
				target.teleport(int(arguments[1]), int(arguments[2]), int(arguments[3]))
				target.message('[Sistema] Voce foi movido por %s' % player.get_name())
				player.message('[Sistema] Personagem movido.')
			else:
				player.message('[Sistema] O personagem esta offline ou nao existe.')
		else:
			player.message('Uso: /move <nome> <mapa> <x> <y>')
			player.message('  ou /move <nome>')
			return True
		return True

commands.register(MoveCommand())