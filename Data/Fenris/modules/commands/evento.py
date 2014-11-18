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
class EventCommand(Command):
	
	# Variaveis
	
	# Constructor
	def __init__(self):
		self.register('/abrirevento', self.command_open)
		self.register('/evento', self.command_go)
		self.register('/fecharevento', self.command_close)
		self.map = 0
		self.pos_x = 125
		self.pos_y = 125
		self.open = False
		self.time = 0
		self.timer = False
		self.players = dict()
		return
		
	# Comando de abrir evento
	def command_open(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 3 or not arguments[0].isdigit() or not arguments[1].isdigit() or not arguments[2].isdigit():
			player.message('Uso: /abrirevento <mapa> <x> <y>')
			return True
		player.message('[Sistema] O evento foi aberto!')
		Server.send_message_all('[Sistema] %s abriu o evento!' % player.get_name())
		self.map = int(arguments[0])
		self.pos_x = int(arguments[1])
		self.pos_y = int(arguments[2])
		self.open = True
		self.players = dict()
		Server.send_announcement_all('[Sistema] Move ativado!')
		Server.send_announcement_all('Digite /evento para participar do evento!')
		self.time = 7
		if self.timer != False:
			timer.clear(self.timer)
		self.timer = timer.repeat(self.timer_callback, 1000, 8)
		return True
	
	def timer_callback(self):
		if (self.time == 0):
			self.open = False
			self.timer = False
			for name in self.players.keys():
				player = Player(self.players[name])
				if (player.get_name() == name):
					if (player.is_playing()):
						player.teleport(self.map, self.pos_x, self.pos_y)
			if self.timer != False:
				timer.clear(self.timer)
				self.timer = False
			Server.send_announcement_all('[Sistema] Move /evento foi desativado, aguarde o proximo evento!')
		else:
			Server.send_announcement_all('[Sistema] Move /evento fecha em %d segundos.' % self.time)
			self.time = self.time - 1
		return

	# Comando para entrar no evento
	def command_go(self, player, arguments):
		if not self.open != False:
			player.message('[Sistema] Nenhum evento aberto no momento.')
		else:
			if not player.get_name() in self.players.keys():
				self.players[player.get_name()] = player.get_index()
				player.message('[Sistema] Voce sera movido em alguns segundos.')
				player.message('No relogue, nao mova ou sera eliminado!')
			else:
				player.message('[Sistema] Voce sera movido em alguns segundos.')
		return True
		
	# Timer de mensagem do sistema
	def command_close(self, player, arguments):
		self.open = False
		self.players = dict()
		Server.send_announcement_all('[Sistema] Move /evento desativado, aguarde o proximo evento.')
		if self.timer != False:
			timer.clear(self.timer)
			self.timer = False
		return True

#
# Initialization
#
commands.register(EventCommand())
