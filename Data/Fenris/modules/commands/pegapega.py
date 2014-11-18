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
class PegaCommand(Command):
	
	# Constructor
	def __init__(self):
		self.register('/iniciarpega-pega', self.command_pega)
		self.register('/abrirpega-pega', self.command_open)
		self.register('/pega-pega', self.command_go)
		self.register('/fimpega-pega', self.command_cancel)
		self.register('/resultadopega-pega', self.command_resultado)
		self.time = 0
		self.timer = False
		self.starttime = 0
		self.starttimer = False
		self.open = False
		self.started = False
		self.players = dict()
		self.participantes = dict()
		self.cancatch = False
		self.teleports = []
		self.teleporttimer = False
		self.firstplace = ''
		self.secondplace = ''
		self.thirdplace = ''
		timer.interval(self.check_participants, 100)
		Events.register('player.move', self.on_move)
		return

	def check_participants(self):
		for part in self.participantes.keys():
			participant = self.participantes[part]
			p = Player(participant)
			if not p.is_playing():
				del self.participantes[part]
				Server.send_message_all('[Sistema] %s tomou dc no pega-pega!' % part)
			else:
				if p.get_map() != 9:
					Server.send_message_all('[Sistema] %s se moveu do pega-pega!' % part)
					del self.participantes[part]
				if p.get_x() < 115 or p.get_y() > 186 or p.get_x() > 155 or p.get_y() < 146:
					Server.send_message_all('[Sistema] %s tentou trapacear!' % part)
					player.teleport(0, 125, 125)
					if player.get_name() in self.participantes:
						del self.participantes[player.get_name()]
					return

		return
	
	def command_resultado(self, player, arguments):
		if not player.is_admin():
			return True
		Server.send_announcement_all('==========================')
		Server.send_announcement_all('[Sistema] Resultado do Pega-Pega:')
		Server.send_announcement_all('Primeiro lugar: %s' % self.firstplace)
		Server.send_announcement_all('Segundo lugar: %s' % self.secondplace)
		Server.send_announcement_all('Terceiro lugar: %s' % self.thirdplace)
		Server.send_announcement_all('==========================')
		return True

	def teleport(self, player):
		self.teleports.append(player)
		if self.teleporttimer != False:
			timer.clear(self.teleporttimer)
		timer.timeout(self.teleport_callback, 500)
		return

	def teleport_callback(self):
		self.teleporttimer = False
		for p in self.teleports:
			player = Player(p)
			player.teleport(0, 125, 125)
		self.teleports = []
		return

	# Comando de abrir evento
	def command_cancel(self, player, arguments):
		if not player.is_admin():
			return True
		self.time = 0
		if self.timer != False:
			timer.clear(self.timer)
		self.timer = False
		self.starttime = 0
		if self.starttimer != False:
			timer.clear(self.starttimer)
		self.starttimer = False
		self.open = False
		self.started = False
		self.players = dict()
		self.participantes = dict()
		self.cancatch = False
		self.teleports = []
		if self.teleporttimer != False:
			timer.clear(self.teleporttimer)
		self.teleporttimer = False
		Server.send_announcement_all('[Sistema] Evento pega-pega finalizado!')
		return True

	# Comando de abrir evento
	def command_pega(self, player, arguments):
		if not player.is_admin():
			return True
		self.starttime = 5
		if self.starttimer != False:
			timer.clear(self.starttimer)
		self.starttimer = timer.repeat(self.command_timer_start, 500, 6)
		return		

	def catch_reset(self):
		self.cancatch = True
		return

	# Timer de mensagem do sistema
	def command_timer_start(self):
		if (self.starttime == 0):
			self.started = True
			self.starttimer = False
			self.cancatch = False
			timer.timeout(self.catch_reset, 500) # 2 segundos e meio pra cada player que for pego
			Server.send_announcement_all('[Sistema] Pega-Pega iniciado!!')
			Server.send_announcement_all('STAFFERS PEGANDO! CORRAMMMMM!!!')
		else:
			Server.send_announcement_all('[Sistema] Pega-Pega inicia em %d...' % self.starttime)
			self.starttime = self.starttime - 1
		return

	# Comando de abrir evento
	def command_open(self, player, arguments):
		if not player.is_admin():
			return True

		if len(arguments) != 1 or not arguments[0].isdigit():
			player.message('Uso: /abrirpega-pega <tempo>')
			return True

		self.time = int(arguments[0])
		
		for i in range(Server.player_start, Server.object_max):
			p = Player(i)
			if p.is_admin():
				continue
			if p.get_map() == 9:
				p.teleport(0, 125, 125)
				
		self.open = True
		self.players = dict()
		self.participantes = dict()
		self.teleports = []
		
		self.firstplace = ''
		self.secondplace = ''
		self.thirdplace = ''

		if self.timer != False:
			timer.clear(self.timer)

		self.timer = timer.repeat(self.command_timer, 1000, self.time + 1)
		player.message('[Sistema] Pega-pega ativado!')
		Server.send_message_all('[Sistema] %s abriu o pega-pega!' % player.get_name())
		Server.send_announcement_all('[Sistema] Move ativado!')
		Server.send_announcement_all('Digite /pega-pega para ir ao evento!')
		return True
	
	# Comando para entrar no evento
	def command_go(self, player, arguments):
		if not self.open != False:
			player.message('[Sistema] Nenhum Pega-Pega aberto no momento.')
		else:
			if not player.is_admin():
				inv = player.get_inventory()
				for i in [0, 1, 2, 3, 4, 5, 7]:
					item = inv.get_item(i)
					if item.is_valid():
						player.message('[Sistema] RETIRE SEUS ITENS!')
						player.message('Somente botas, aneis e pendants sao permitidos.')
						return True
				item = inv.get_item(8)
				if item.is_valid():
					if item.is_item(13, 3) or item.is_item(13, 2):
						player.message('[Sistema] RETIRE SEUS ITENS!')
						player.message('Somente botas, aneis e pendants sao permitidos.')
						return True

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
			self.started = False
			self.participantes = dict()
			self.teleports = []
			for name in self.players.keys():
				player = Player(self.players[name])
				if (player.get_name() == name):
					if (player.is_playing()):
						player.teleport(9, 150, 150)
						if not player.is_admin():
							self.participantes[player.get_name()] = player.get_index()

			Server.send_announcement_all('[Sistema] Move /pega-pega desativado!')
			Server.send_announcement_all('aguarde o proximo evento.')
			Server.send_announcement_all('CORRAAAAAMMMMM!!!!')
		else:
			Server.send_announcement_all('[Sistema] Move /pega-pega fecha em %d segundos!' % self.time)
			self.time = self.time - 1
		return

	# Comando pega
	def on_move(self, index, map, sx, sy, tx, ty):
		if not self.started:
			return

		player = Player(index)
		if map != 9:
			return

		if tx < 115 or ty > 186 or tx > 155 or ty < 146:
			player.message('[Sistema] Movido por nao estar na area do evento!')
			player.teleport(0, 125, 125)
			if player.get_name() in self.participantes:
				del self.participantes[player.get_name()]
			return

		if not player.is_admin():
			return

		if self.cancatch:
			pls = []
			for i in player.get_near_players():
				dist = Server.get_distance(index, i)
				if dist == -1:
					continue
				if dist <= 3:
					pls.append(i)

			if len(pls) > 0:
				target_index = random.choice(pls)
				target = Player(target_index)

				if target.get_name() in self.participantes:
					del self.participantes[target.get_name()]

					Server.apply_skill(player.get_index(), target.get_index(), 3) # Lightning
					target.message('[Sistema] Voce foi pego por %s' % player.get_name())
					player.message('[Sistema] Voce pegou %s' % target.get_name())

					self.cancatch = False
					timer.timeout(self.catch_reset, 500) # 1 segundo e meio pra cada player que for pego

					self.teleport(target.get_index())

					if len(self.participantes) > 2:
						Server.send_announcement_all('[Sistema] %s pego por %s' % (target.get_name(), player.get_name()))
					elif len(self.participantes) == 2:
						Server.send_announcement_all('[Sistema] %s pego por %s' % (target.get_name(), player.get_name()))
						Server.send_announcement_all('  (terceiro lugar)  ')
						self.thirdplace = target.get_name()
					elif len(self.participantes) == 1:
						Server.send_announcement_all('%s pego por %s' % (target.get_name(), player.get_name()))
						Server.send_announcement_all('  (segundo lugar)  ')
						self.secondplace = target.get_name()
						ks = self.participantes.keys()
						winner = Player(self.participantes[ks[0]])
						Server.send_announcement_all('==========================')
						Server.send_announcement_all('[Sistema] %s venceu o pega-pega!' % winner.get_name())
						Server.send_announcement_all('==========================')
						self.firstplace = winner.get_name()
					elif len(self.participantes) == 0 and self.firstplace == '':
						Server.send_announcement_all('==========================')
						Server.send_announcement_all('[Sistema] %s venceu o pega-pega!' % target.get_name())
						Server.send_announcement_all('==========================')
						self.firstplace = target.get_name()

		return

#
# Initialization
#
commands.register(PegaCommand())