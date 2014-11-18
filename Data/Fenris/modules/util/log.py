#
# Imports
#
from wolfulus import *
from player import *
from datetime import *
import hashlib

#
# Handler class
#
class ChatLog(object):

	#
	# Constructor
	#
	def __init__(self):
		Console.write('Instalando chat logging...')
		Events.register('player.message', self.message)
		Events.register('player.whisper', self.whisper)
		return

	#
	# Logging
	#
	def log(self, filename, msg, type):
		dt = datetime.now()
		currtime = dt.strftime("%I:%M%p")
		m = hashlib.md5()
		m.update(filename)
		f = open('./Log/CHAT_%s.txt' % (m.hexdigest()), 'a')
		f.write('[%s] %s\n' % (currtime, msg))
		f.close()
		if type != '':
			Console.warn('[%s] %s' % (type, msg))
		return
		
	#
	# Chat handler
	#
	def message(self, index, text):
		player = Player(index)
		self.log(player.get_name(), '%s: %s' % (player.get_name(), text), 'CHAT')
		return False

	#
	# Whisper handler
	#
	def whisper(self, index, target, text):
		player1 = Player(index)
		player2 = Player(target)
		self.log(player1.get_name(), '%s -> %s: %s' % (player1.get_name(), player2.get_name(), text), '')
		self.log(player2.get_name(), '%s -> %s: %s' % (player1.get_name(), player2.get_name(), text), 'WHISP')
		return False

#
# Command handler instance
#
chatlog = ChatLog()