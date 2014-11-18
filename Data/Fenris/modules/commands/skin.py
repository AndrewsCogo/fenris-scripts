#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import * 

#
# Comando para troca de skins
#
class SkinCommand(Command):
	
	# Constructor
	def __init__(self):
		self.register('/skin', self.command_skin)
		return
		
	# Comando de skin
	def command_skin(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 2:
			player.message('Uso: /skin <nome> <monstro>')
			return True
		index = Server.find_by_name(arguments[0])
		if (index >= 0):
			target = Player(index)
			target.set_skin(int(arguments[1]))
			target.message('[Sistema] Voce recebeu uma Skin de %s' % player.get_name())
			player.message('[Sistema] Personagem transformado.')
		else:
			player.message('[Sistema] O personagem esta offline ou nao existe.')
		return True

#
# Registro global
#
commands.register(SkinCommand())
