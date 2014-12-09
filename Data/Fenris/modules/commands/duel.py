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
		self.players = [player1, player2]
		Events.register('player.kill', self.event_kill)
		
	# pega o primeiro jogador
	def get_first_player(self):
		return self.players[0]
		
	# pega o segundo jogador
	def get_second_player(self):
		return self.players[1]
		
	def event_kill(self, id1, id2):
		player1 = Player(id1)
		player2 = Player(id2)
		#if player1.get_name() == self.get_first_player().get_name():
		#if player2.get_name() == self.get_second_player().get_name():
				
				
		
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
		self.requests = dict() 
		self.register('/duelo', self.command_duel)
		self.register('/aceitar', self.command_accept)
		self.register('/recusar', self.command_refuse)
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
			
			for name in self.requests:
				if self.requests[name].get_target_name() == target.get_name():
					self.requests[name].get_source().message('[Sistema] Desculpe, mas o jogador %s aceitou o duelo com outra pessoa.' % target.get_name())
					self.requests[name].clear_timeout()
					del self.requests[name]		
			
		else:
			player.message('[Sistema] Este jogador nao pediu duelo com voce.')
			return True	
			
		return True
		
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
			
		target.message('[Sistema] %s enviou um pedido de duelo.' % player.get_name())
		target.message('[Sistema] Digite "/aceitar %s" para aceitar.' % player.get_name())
		target.message('[Sistema] Digite "/recusar %s" para recusar ou aguarde 10 segundos.' % player.get_name())
		player.message('[Sistema] Pedido enviado para %s' % target.get_name())
		
		request = DuelRequest(player, target)
		request.on_timeout(self.request_timeout)
		self.requests[player.get_name()] = request
		return True
		
	def request_timeout(self, request):
		target = request.get_target()
		target_name = request.get_target_name()
		source = request.get_source()
		source_name = request.get_source_name()
		if source_name in self.requests:
			source.message('[Sistema] Seu pedido de duelo contra %s expirou.' % target_name)
			target.message('[Sistema] Pedido de duelo de %s expirou.' % source_name)
			del self.requests[source_name]

#
# Initialization
#
commands.register(DuelCommand())
