#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import *
from ..util.timer import *

#
# Command
#
class BloqueioCommand(Command):

	# Constructor
	def __init__(self):
		self.register('/blockareapvp', self.command_abrir)
		self.register('/desblockareapvp', self.command_fechar)
		Events.register('player.move', self.on_move)
		timer.interval(self.pvp_check, 1000)
		self.players = dict()
		self.avisados = []
		self.open = False
		return

	# Verifica se ta dentro da area de pvp
	def pvp_area(self, map, x, y):
		if map == 6:
			if (x >= 51 and y >= 146) and (x <= 75 and y <= 202):
				if (x >= 62 and y >= 171) and (x <= 64 and y <= 175):
					return False
				return True
		return False

	# Timer de checagem pvp
	def pvp_check(self):
		for index in self.players.keys():
			player = Player(index)
			time = self.players[index]
			
			if not player.is_playing():
				del self.players[index]
				continue

			if player.is_admin():
				del self.players[index]
				continue

			if time > 0:
				player.message('[Sistema] Voce tem %d segundos para sair da area PVP!' % time)
				time = time - 1
				self.players[index] = time
			else:
				if time == 0:
					player.teleport(0, 125, 125)
					Server.send_announcement_all('[Sistema]')
					Server.send_announcement_all('%s movido por ficar na area PVP!' % player.get_name())
					del self.players[index]
				else:
					time = time - 1
					self.players[index] = time
		return

	# Movimento
	def on_move(self, index, map, sx, sy, tx, ty):
		player = Player(index)
		if self.open:
			if self.pvp_area(map, tx, ty):
				if not player.is_admin():
					if self.avisados.count(index) > 0 and not index in self.players.keys():
						player.teleport(0, 125, 125)
						Server.send_announcement_all('[Sistema]')
						Server.send_announcement_all('%s movido por entrar na area PVP apos ser avisado!' % player.get_name())
					if not index in self.players.keys():
						self.avisados.append(index)
						player.message('[Sistema] Saia da area de PVP ou sera movido!')
						self.players[index] = 3
			else:
				if index in self.players:
					player.message('[Sistema] Voce sera movido se ultrapassar a faixa vermelha novamente!')
					del self.players[index] 
		return
	
	# Comando de abrir evento
	def command_abrir(self, player, arguments):
		if not player.is_admin():
			return True
		Server.send_announcement_all('[Sistema] %s bloqueou a area de PVP.' % player.get_name())
		Server.send_announcement_all('Quem ultrapassar a faixa vermelha')
		Server.send_announcement_all('sera movido automaticamente!')
		Server.send_message_all('[Sistema] Nao entre na area de PVP ou sera movido!')
		self.players = dict()
		self.avisados = []
		for i in range (Server.player_start, Server.object_max):
			p = Player(i)
			if p.is_admin():
				continue
			if self.pvp_area(p.get_map(), p.get_x(), p.get_y()):
				self.players[p.get_index()] = 15
				self.avisados.append(p.get_index())
				p.message('[Sistema] ATENCAO: Saia da area de PVP ou sera movido!')
		self.open = True
		return True

	# Comando de fechar evento
	def command_fechar(self, player, arguments):
		if not player.is_admin():
			return True
		Server.send_announcement_all('[Sistema] %s liberou a area de PVP.' % player.get_name())
		Server.send_announcement_all('O acesso a area esta disponivel!')
		self.players = dict()
		self.avisados = []
		self.open = False
		return True

#
# Initialization
#
commands.register(BloqueioCommand())