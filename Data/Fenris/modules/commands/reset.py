#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import * 
from ..util.timer import * 

#
# Comando para troca de skins
#
class ResetCommand(Command):
	
	#
	# Constructor
    #
	def __init__(self):
		self.npcs = []
		self.register('/resetar', self.command_reset)
		self.register('/reset', self.command_reset)
		Events.register('monster.reload', self.monster_reload)
		Events.register('npc.talk', self.npc_talk)
		timer.timeout(self.init_npc, 30000)
		return

	#
	# Monster reload
	#
	def monster_reload(self):
		self.init_npc()
		return

	#
	# Npc
	#
	def init_npc(self):
		self.npcs = []
		self.npcs.append(Map(0).spawn(247, 126, 145, 1))
		self.npcs.append(Map(2).spawn(247, 226, 62, 1)) 
		return

	#
	# Npc Talk
	#
	def npc_talk(self, player, npc):
		if self.npcs.count(npc) > 0:
			p = Player(player)
			if not self.reset(p):
				Server.npc_message(player, npc, 'Level insuficiente!')
			else:
				Server.npc_message(player, npc, 'Parabens, voce resetou!')
			return True
		return False

	#
	# Resets o personagem
	#
	def reset(self, player):
		if player.is_vip():
			if player.get_level() >= 300:
				player.increment_resets()
				player.set_level(50)
				player.set_exp(0)
			else:
				return False
		else:
			if player.get_level() >= 500:
				player.increment_resets()
				player.set_level(1)
				player.set_map(0)
				player.set_x(125)
				player.set_y(125)
			else:
				return False
		player.select_character()
		return True
	
	#	
	# Comando de reset
	#
	def command_reset(self, player, arguments):
		if not self.reset(player):
			player.message('Level insuficiente!')
		else:
			player.message('Parabens, voce resetou!') 
		return True

#
# Registro global
#
commands.register(ResetCommand())
