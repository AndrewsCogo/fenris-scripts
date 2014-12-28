#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import *
from ..util.timer import *
import random

#
# Command
#
class MataMataCommand(Command):

	# Constantes... nao mexer
	UP = 1
	DOWN = 2

	# Constructor
	def __init__(self):
		self.register('/chamar', self.command_chamar)
		self.register('/regrasmt', self.command_regras)
		self.register('/fase', self.command_fase_generico)
		self.register('/semi', self.command_semi)
		self.register('/disputa3', self.command_disputa)
		self.register('/final', self.command_final)
		self.register('/abrirnovaarena', self.command_open)
		self.register('/novaarena', self.command_go)
		self.register('/wins', self.command_finalizar)
		self.time = 0
		self.timer = False
		self.open = False
		self.players = dict()
		self.lado = self.UP
		self.fighter1 = None
		self.fighter2 = None
		return

	# Comando finalizar
	def command_finalizar(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 1:
			player.message('Uso: /wins <nome do vencedor>')
			return True
		if (self.fighter1 is None or self.fighter2 is None):
			player.message('[Sistema] Nenhuma luta foi realizada.')
			return True
		index = Server.find_by_name(arguments[0])
		if (index >= 0):
			target = Player(index)
			self.switch_sides(target)
			Server.send_announcement_all('%s wins' % target.get_name())
			if (target.get_name() == self.fighter1.get_name()):
				self.fighter2.teleport(0, 125, 125)
			elif (target.get_name() == self.fighter2.get_name()):
				self.fighter1.teleport(0, 125, 125)
		return True

	# Comando de abrir evento
	def command_open(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 1 or not arguments[0].isdigit():
			player.message('Uso: /abrirnovaarena <tempo>')
			return True

		self.time = int(arguments[0])
		self.open = True
		self.players = dict()
		self.lado = self.UP
		self.fighter1 = None
		self.fighter2 = None

		if self.timer != False:
			timer.clear(self.timer)

		self.timer = timer.repeat(self.command_timer, 1000, self.time + 1)
		player.message('[Sistema] Nova Arena foi aberta!')
		Server.send_message_all('[Sistema] %s abriu Nova Arena!' % player.get_name())
		Server.send_announcement_all('[Sistema] Move ativado!')
		Server.send_announcement_all('Digite /novaarena para ir ao evento!')
		return True
	
	# Comando para entrar no evento
	def command_go(self, player, arguments):
		if self.open == False:
			player.message('[Sistema] Nova Arena nao esta aberta no momento.')
		else:
			if not player.get_name() in self.players.keys():
				self.players[player.get_name()] = player.get_index()
				player.message('[Sistema] Voce sera movido em alguns segundos..')
				player.message('Nao relogue, nao mova ou sera eliminado!')
			else:
				player.message('[Sistema] Voce sera movido em alguns segundos..')
		return True
		
	# Timer de mensagem do sistema
	def command_timer(self):
		if (self.time == 0):
			self.open = False
			self.timer = False
			for name in self.players.keys():
				player = Player(self.players[name])
				if (player.get_name() == name):
					if (player.is_playing()):
						player.teleport(6, 60, 210)
			Server.send_announcement_all('[Sistema] Move /novaarena foi desativado, aguarde o proximo evento!')
		else:
			Server.send_announcement_all('[Sistema] Move /novaarena fecha em %d segundos.' % self.time)
			self.time = self.time - 1
		return

	# Area de espera de baixo
	def waiting_area_up(self, x, y):
		if (x >= 50 and y >= 180):
			if (x <= 75 and y <= 230):
				return True
		return False

	# Area de espera de cima
	def waiting_area_down(self, x, y):
		if (x >= 50 and y >= 122):
			if (x <= 75 and y <= 160):
				return True
		return False

	# Sends a player to the other side
	def switch_sides(self, player):
		if self.lado == self.DOWN:
			player.teleport(6, 60, 210)
		elif self.lado == self.UP:
			player.teleport(6, 60, 140)
		return

	# Is on waiting area
	def is_on_waiting_area(self, player):
		if player.get_map() == 6:
			if self.lado == self.UP:
				if self.waiting_area_up(player.get_x(), player.get_y()):
					return True
			elif self.lado == self.DOWN:
				if self.waiting_area_down(player.get_x(), player.get_y()):
					return True
		return False

	# Comando de abrir evento
	def command_chamar(self, player, arguments):
		if not player.is_admin():
			return True

		players = []
		for i in range(Server.player_start, Server.object_max):
			p = Player(i)
			if p.is_admin():
				continue
			if not p.is_playing():
				continue
			if self.is_on_waiting_area(p):
				players.append(i)

		if len(players) > 1:
		
			random.shuffle(players)
		
			p1 = players[0]
			players.pop(0)

			p2 = players[0]
			players.pop(0)

			player1 = Player(p1)
			player1.teleport(6, 63, 172)
			player1.message('[Sistema] Sua vez, prepare-se para a luta!')
			self.fighter1 = player1

			player2 = Player(p2)
			player2.teleport(6, 63, 173)
			player2.message('[Sistema] Sua vez, prepare-se para a luta!')
			self.fighter2 = player2
			
			Server.send_message_all('[Sistema] %s chamou a proxima luta!' % player.get_name())
			player.message('[Sistema] Restam (%d) jogadores para lutar!' % len(players))
			Server.send_announcement_all('<< [%s] >>' % player.get_name())
			Server.send_announcement_all('%s vs %s' % (player1.get_name(), player2.get_name()))
		elif len(players) == 1:
			p = Player(players[0])
			self.switch_sides(p)
			Server.send_announcement_all('%s passa para a proxima fase por falta de adversario.' % p.get_name())
			player.message('[Sistema] Todos os jogadores ja lutaram!')
			player.message('Avance de fase para prosseguir com o evento!!')
		else:
			player.message('[Sistema] Todos os jogadores ja lutaram!')
			player.message('Avance de fase para prosseguir com o evento!!')
		return True

	# Comando de abrir evento
	def command_regras(self, player, arguments):
		if not player.is_admin():
			return True
		player.message('[Sistema] As regras foram ditas!')
		Server.send_message_all('[Sistema] %s passou as Regras! Leia o global.' % player.get_name())
		Server.send_announcement_all('[Sistema] Regras do evento:')
		Server.send_announcement_all('- Lutas de 1 round, final com 3 rounds.')
		Server.send_announcement_all('- Andou, TS, Antes=infracao / 2=eliminado!')
		Server.send_announcement_all('- Entrou na area de PVP = movido!')
		Server.send_announcement_all('- Nao fique away, nao vamos esperar voltar!')
		Server.send_announcement_all('----> Use /re off , Boa sorte! <----')
		return True

	# Mensagem fase
	def command_fase(self, player, fase):
		player.message('[Sistema] Fase %d iniciada!' % (fase))
		Server.send_announcement_all('==========================')
		Server.send_announcement_all('~ Fase (%d) do Mata-Mata iniciada! ~' % (fase))
		Server.send_announcement_all('==========================')
		return True

	# Comando de fase
	def command_fase_generico(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 1 or not arguments[0].isdigit():
			player.message('Uso: /fase <numero_da_fase>')
			return True
		fase = int(arguments[0])
		if fase % 2 == 1:
			self.lado = self.UP
		else:
			self.lado = self.DOWN
		self.command_fase(player, int(arguments[0]))
		return True

	# Comando de semi final
	def command_semi(self, player, arguments):
		if not player.is_admin():
			return True
		player.message('[Sistema] Fase semi-final iniciada!')
		Server.send_announcement_all('==========================')
		Server.send_announcement_all('~ Semi-Final do Mata-Mata iniciada! ~')
		Server.send_announcement_all('   Regras: 2 Rounds, matou = 2x Stabs   ')
		Server.send_announcement_all('==========================')
		if self.lado == self.UP:
			self.lado = self.DOWN
		else:
			self.lado = self.UP
		return True
	
	# Comando de disputa
	def command_disputa(self, player, arguments):
		if not player.is_admin():
			return True
		player.message('[Sistema] Disputa do terceiro lugar iniciada!')
		Server.send_announcement_all('==========================')
		Server.send_announcement_all('~ Disputa do terceiro lugar iniciada! ~')
		Server.send_announcement_all('   Regras: 2 Rounds, matou = 2x Stabs   ')
		Server.send_announcement_all('==========================')
		if self.lado == self.UP:
			self.lado = self.DOWN
		else:
			self.lado = self.UP
		return True
	
	# Comando de final
	def command_final(self, player, arguments):
		if not player.is_admin():
			return True
		player.message('[Sistema] Fase final iniciada!')
		Server.send_announcement_all('==========================')
		Server.send_announcement_all('~ Final do Mata-Mata iniciada! ~')
		Server.send_announcement_all('   Regras: 3 Rounds, matou = 2x Stabs   ')
		Server.send_announcement_all('==========================')
		if self.lado == self.UP:
			self.lado = self.DOWN
		else:
			self.lado = self.UP
		return True

#
# Initialization
#
commands.register(MataMataCommand())