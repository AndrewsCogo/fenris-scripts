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
class PkCommand(Command):
	
	#
	# Constructor
    #
	def __init__(self):
		self.npcs = []
		self.register('/pk', self.command_pk)
		self.register('/pkclear', self.command_pk)
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
		self.npcs.append(Map(0).spawn(249, 128, 145, 1))
		self.npcs.append(Map(2).spawn(249, 228, 62, 1))
		return

	#
	# Npc Talk
	#
	def npc_talk(self, player, npc):
		if self.npcs.count(npc) > 0:
			p = Player(player)
			msg = 'Seu PK foi limpo!'
			if p.get_pklevel() < 3:
				msg = 'Seu Hero foi limpo!'
			if not self.pkclear(p):
				Server.npc_message(player, npc, 'Voce nao eh nem PK nem Hero!')
			else:
				Server.npc_message(player, npc, msg)
			return True
		return False

	#
	# PkClear
	#
	def pkclear(self, player):
		if player.get_pklevel() != 3:
			player.set_pklevel(3)
			player.set_pkcount(0)
			player.set_pktime(0)
			return True
		else:
			return False
	#	
	# Comando de reset
	#
	def command_pk(self, player, arguments):
		msg = 'Seu PK foi limpo!'
		if player.get_pklevel() < 3:
			msg = 'Seu Hero foi limpo!'
		if not self.pkclear(player):
			player.message('Voce nao eh nem PK nem Hero!')
		else:
			player.message(msg) 
		return True

#
# Registro global
#
commands.register(PkCommand())

