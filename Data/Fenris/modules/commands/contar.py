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
class ContarCommand(Command):
	
	# Variaveis
	
	# Constructor
	def __init__(self):
		self.register('/contar', self.command_open)
		self.time = 0
		self.timer = False
		self.players = dict()
		return
		
	# Comando de abrir evento
	def command_open(self, player, arguments):
		if not player.is_admin():
			return True
		if len(arguments) != 1:
			player.message('Uso: /contar <tempo em segundos>')
			return True
		Server.send_announcement_all('< %s >' % player.get_name())
		Server.send_announcement_all('Preparar...')
		self.time = int(arguments[0]) - 1
		if self.timer != False:
			timer.clear(self.timer)
		self.timer = timer.repeat(self.timer_callback, 1000, int(arguments[0]))
		return True
	
	def timer_callback(self):
		if (self.time == 0):
			Server.send_announcement_all('JA!!')
		else:
			Server.send_announcement_all('%d' % self.time)
			self.time = self.time - 1
		return

#
# Initialization
#
commands.register(ContarCommand())
