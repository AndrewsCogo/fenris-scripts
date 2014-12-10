#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import *
from ..util.inventory import * 
from ..util.item import * 
from datetime import datetime
from ..util.timer import * 
import random

#
# instancia do duelo
#
class Duel:

	# constructor
	def __init__(self, player1, player2):
		self.points = dict()
		self.players = [player1, player2]
		self.points[player1.get_name()] = 0
		self.points[player2.get_name()] = 0
		self.finish_callback = None
		timer.timeout(self.start, 5000)
		self.respawn_id = None
		self.respawn_map = player2.get_map()
		self.respawn_x = player2.get_x()
		self.respawn_y = player2.get_y()
		self.duel_time = 3
		player1.message('[Sistema] O duelo comecara em 5 segundos...')
		player1.message('[Sistema] Tempo maximo do duelo: %d minutos' % self.duel_time)
		player2.message('[Sistema] O duelo comecara em 5 segundos...')
		player2.message('[Sistema] Tempo maximo do duelo: %d minutos' % self.duel_time)
		
	def respawn(self):
		if self.respawn_id != None:
			timer.clear(self.respawn_id)
			self.respawn_id = None
		self.respawn_id = timer.timeout(self.respawn_callback, 1000 * 8) # 8 segundos para o respawn
		
	def respawn_callback(self):
		self.respawn_id = None
		self.players[0].teleport(self.respawn_map, self.respawn_x, self.respawn_y)
		self.players[1].teleport(self.respawn_map, self.respawn_x, self.respawn_y)
		self.players[0].message('[Sistema] Lutem!')
		self.players[1].message('[Sistema] Lutem!')
		
	def start(self):
		tempo = (1000 * 60) * self.duel_time		
		self.timer = timer.timeout(self.finish, tempo)
		self.respawn_callback()
		
	def finish(self):
	
		if self.timer != None:
			timer.clear(self.timer)
			self.timer = None
			
		self.players[0].message('[Sistema] Duelo encerrado.')
		self.players[1].message('[Sistema] Duelo encerrado.')
		
		player1 = self.players[0]
		player2 = self.players[1]
		
		pontos1 = self.points[self.players[0].get_name()]
		pontos2 = self.points[self.players[1].get_name()]
		
		if pontos1 == pontos2:			
			self.players[0].message('[Sistema] Resultado: empatado com %d pontos' % pontos1)
			self.players[1].message('[Sistema] Resultado: empatado com %d pontos' % pontos1)
			if self.finish_callback != None:
				self.finish_callback(self, None)
		else:
			pontos = pontos1
			winner = player1
			looser = player2
			if pontos2 > pontos1:
				pontos = pontos2
				winner = player2
				looser = player1		
			self.players[0].message('[Sistema] Resultado: %s venceu com %d pontos' % (winner.get_name(), pontos))
			self.players[1].message('[Sistema] Resultado: %s venceu com %d pontos' % (winner.get_name(), pontos))
			if self.finish_callback != None:
				self.finish_callback(self, winner)
		
	def on_finish(self, callback):
		self.finish_callback = callback
		
	def event_kill(self, id1, id2):
		killer = Player(id1)
		victim = Player(id2)	
		
		if not (killer.get_name() == self.players[0].get_name() and victim.get_name() == self.players[1].get_name()):
			if not (victim.get_name() == self.players[0].get_name() and killer.get_name() == self.players[1].get_name()):
				return
		
		if self.respawn_id != None:			
			killer.message('[Sistema] Nao valeu! Aguarde o respawn.')
			victim.message('[Sistema] Nao valeu! %s nao aguardou o respawn.' % killer.get_name())
			self.respawn()
			return
		
		pontos = self.points[killer.get_name()]
		pontos = pontos + 1
		self.points[killer.get_name()] = pontos
				
		victim.message('[Sistema] %s marcou um ponto' % killer.get_name())
		killer.message('[Sistema] Voce marcou um ponto')	

		if pontos >= 3:
			self.finish()
		else:
			self.respawn()
		
		
class DuelRequest:

	def __init__(self, source, target):
		self.source = source
		self.source_name = source.get_name() 
		self.target = target
		self.target_name = target.get_name()
		self.timeout_id = timer.timeout(self.timeout, 1000 * 10) # 10 segundos
		self.timeout_callback = None
		
	# pega o jogador que pediu o duel
	def get_source(self):
		return self.source
	def get_source_name(self):
		return self.source_name
		
	# pega o jogador que recebeu o pedido
	def get_target(self):
		return self.target
	def get_target_name(self):
		return self.target_name
		
	def on_timeout(self, callback):
		self.timeout_callback = callback
		
	def clear_timeout(self):
		if self.timeout_id != None:
			timer.clear(self.timeout_id)
			self.timeout_id = None
			
	def timeout(self):
		if self.timeout_callback != None:
			self.timeout_callback(self)
		
		
#
# command
#	
class DuelCommand(Command):
	
	def __init__(self):
		self.duels = []
		self.requests = dict() 
		self.register('/duel', self.command_duel)
		self.register('/aceitar', self.command_accept)
		self.register('/recusar', self.command_refuse)
		Events.register('player.kill', self.event_kill)
		return
		
	def command_accept(self, player, arguments):
		target = player
		
		if len(arguments) != 1:
			player.message('[Sistema] Uso: /aceitar <nome>')
			return True
			
		if arguments[0] in self.requests:
			request = self.requests[arguments[0]]
			if request.get_target_name() != target.get_name():
				target.message('[Sistema] Este jogador nao pediu duelo com voce.')
				return True			
			
			source = Server.find_by_name(arguments[0])
			if source < 0:
				target.message('[Sistema] Este jogador esta offline ou nao existe.')
				self.requests[arguments[0]].clear_timeout()
				del self.requests[arguments[0]]
				return True
				
			source = Player(source)		
			
			source.message('[Sistema] Duelo aceito. Teleportando voce para o jogador.')
			source.teleport(target.get_map(), target.get_x(), target.get_y())
			
			self.requests[arguments[0]].clear_timeout()
			del self.requests[arguments[0]]
			
			names_to_delete = []
			for name in self.requests:
				if self.requests[name].get_target_name() == target.get_name():
					self.requests[name].get_source().message('[Sistema] Desculpe, mas o jogador %s aceitou o duelo com outra pessoa.' % target.get_name())
					self.requests[name].clear_timeout()
					names_to_delete.append(name)
			
			for name in names_to_delete:
				del self.requests[name]		
										
			duel = Duel(source, target)
			duel.on_finish(self.duel_finish)
			self.duels.append(duel)
			
		else:
			player.message('[Sistema] Este jogador nao pediu duelo com voce.')
			return True	
			
		return True
		
	def duel_finish(self, duel, winner, looser):
		self.remove_duel(duel)
		if winner != None:
			winner.increase_duel_wins()
		if looser != None:
			looser.increase_duel_losses()
		
	def remove_duel(self, duel):
		for key in range(len(self.duels)):
			d = self.duels[key]
			if d.players[0].get_name() == duel.players[0].get_name() and d.players[1].get_name() == duel.players[1].get_name():
				del self.duels[key]
				return
		
	def command_refuse(self, player, arguments):
			
		target = player
		
		if len(arguments) != 1:
			player.message('[Sistema] Uso: /recusar <nome>')
			return True
			
		if arguments[0] in self.requests:
			request = self.requests[arguments[0]]
			if request.get_target_name() != target.get_name():
				target.message('[Sistema] Este jogador nao pediu duelo com voce.')
				return True			
			
			source = Server.find_by_name(arguments[0])
			if source < 0:
				target.message('[Sistema] Este jogador esta offline ou nao existe.')
				self.requests[arguments[0]].clear_timeout()
				del self.requests[arguments[0]]
				return True
				
			source = Player(source)		
			
			source.message('[Sistema] %s recusou o seu pedido de duelo' % target.get_name())
			target.message('[Sistema] Voce recusou o duelo contra %s' % source.get_name())
						
			self.requests[source.get_name()].clear_timeout()
			del self.requests[source.get_name()]
			
		else:
			player.message('[Sistema] Este jogador nao pediu duelo com voce.')
			return True	
			
		return True
		
	def command_duel(self, player, arguments):		
		if player.get_name() in self.requests:
			player.message('[Sistema] Pedido para %s ainda esta pendente. Aguarde.' % self.requests[player.get_name()].get_target_name())
			return True
			
		if len(arguments) != 1:
			player.message('[Sistema] Uso: /duel <nome>')
			return True
			
		target = Server.find_by_name(arguments[0])
		if target < 0:
			player.message('[Sistema] Este jogador esta offline ou nao existe.')
			return True
			
		target = Player(target)		
		if player.get_name() == target.get_name():
			player.message('[Sistema] Voce nao pode pedir duelo pra si mesmo.')
			return True
		
		if target.get_name() in self.requests:
			player.message('[Sistema] Este jogador esta tentando duelar contra outra pessoa.')
			return True
			
		if self.in_duel(target.get_name()):
			player.message('[Sistema] Este jogador ja esta duelando com outra pessoa.')
			return True
			
		target.message('[Sistema] %s enviou um pedido de duelo.' % player.get_name())
		target.message('[Sistema] Digite "/aceitar %s" para aceitar.' % player.get_name())
		target.message('[Sistema] Digite "/recusar %s" para recusar ou aguarde 10 segundos.' % player.get_name())
		player.message('[Sistema] Pedido enviado para %s' % target.get_name())
		
		request = DuelRequest(player, target)
		request.on_timeout(self.request_timeout)
		self.requests[player.get_name()] = request
		return True
		
	def in_duel(self, name):
		for duel in self.duels:
			if (duel.players[0].get_name() == name or duel.players[1].get_name() == name):
				return True
		return False
			
	def request_timeout(self, request):
		target = request.get_target()
		target_name = request.get_target_name()
		source = request.get_source()
		source_name = request.get_source_name()
		if source_name in self.requests:
			source.message('[Sistema] Seu pedido de duelo contra %s expirou.' % target_name)
			target.message('[Sistema] Pedido de duelo de %s expirou.' % source_name)
			del self.requests[source_name]
			
	def event_kill(self, id1, id2):
		for key in range(len(self.duels)):
			self.duels[key].event_kill(id1, id2)

#
# Initialization
#
commands.register(DuelCommand())
