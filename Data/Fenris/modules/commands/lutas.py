#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import *
from ..util.inventory import * 
from ..util.item import * 
#
# Command
#
class DevCommands(Command):
	
	def __init__(self):
		self.register('/vs', self.vs)
		self.register('/winscima', self.cima)
		self.register('/winsbaixo', self.baixo)
		self.register('/proximo', self.proximo)
		return

	def vs(self, player, arguments):
		if not player.is_admin():
			return True

		if len(arguments) != 2:
			player.message('Uso: /vs <Player1> <Player2>')
			return True

		player1 = Server.find_by_name(arguments[0])
		if player1 < 0:
			player.message('[Sistema] %s nao esta online ou nao existe.' % arguments[0])
			return True
		player2 = Server.find_by_name(arguments[1])
		if player2 < 0:
			player.message('[Sistema] %s nao esta online ou nao existe.' % arguments[1])
			return True

		p1 = Player(player1)
		p1.message('[Sistema] Sua vez! Prepare-se e boa sorte!!')
		p1.teleport(6, 63, 172)

		p2 = Player(player2)
		p2.teleport(6, 63, 173)		
		p2.message('[Sistema] Sua vez! Prepare-se e boa sorte!!')
		Server.send_announcement_all('[%s]' % player.get_name())
		Server.send_announcement_all('%s vs %s' % (arguments[0], arguments[1]))
		return True

	def proximo(self, player, arguments):
		if not player.is_admin():
			return True

		if len(arguments) != 1:
			player.message('Uso: /proximo <Player>')
			return True

		player1 = Server.find_by_name(arguments[0])
		if player1 < 0:
			target.message('[Sistema] %s nao esta online ou nao existe.' % arguments[0])
			return True

		p1 = Player(player1)
		p1.teleport(6, 63, 173)	
		p1.message('[Sistema] Sua vez! Prepare-se e boa sorte!!')
		Server.send_announcement_all('[%s]' % player.get_name())
		Server.send_announcement_all('Proximo lutador: %s' % arguments[0])
		return True
		
	def cima(self, player, arguments):
		if not player.is_admin():
			return True

		if len(arguments) != 1:
			player.message('Uso: /winscima <Player>')
			return True

		player1 = Server.find_by_name(arguments[0])
		if player1 < 0:
			target.message('[Sistema] %s nao esta online ou nao existe.' % arguments[0])
			return True
		
		p1 = Player(player1)
		p1.teleport(6, 60, 210)	
		p1.message('[Sistema] Voce venceu a luta! Parabens!!')
		Server.send_announcement_all('%s wins' % arguments[0])
		return True

	def baixo(self, player, arguments):
		if not player.is_admin():
			return True

		if len(arguments) != 1:
			player.message('Uso: /winsbaixo <Player>')
			return True

		player1 = Server.find_by_name(arguments[0])
		if player1 < 0:
			target.message('[Sistema] %s nao esta online ou nao existe.' % arguments[0])
			return True
		
		p1 = Player(player1)
		p1.teleport(6, 62, 140)	
		p1.message('[Sistema] Voce venceu a luta! Parabens!!')
		Server.send_announcement_all('%s wins' % arguments[0])
		return True

#
# Initialization
#
commands.register(DevCommands())
