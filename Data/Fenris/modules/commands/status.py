#
# Imports
#
from wolfulus import *
from ..util.player import *
from ..util.chat import *

#
# Command
#
class StatusCommand(Command):
	
	# Variables
	maximum = 32767

	# Constructor
	def __init__(self):
		self.register('/f', self.add_strength)
		self.register('/a', self.add_dexterity)
		self.register('/v', self.add_vitality)
		self.register('/e', self.add_energy)
		Events.register('player.addpoint', self.add_point)
		return 
	
	#	
	# Strength
	#
	def add_strength(self, player, arguments):
		if len(arguments) != 1:
			player.message('[Sistema] Uso: /f <pontos>')
		else:
			points = int(arguments[0])
			if player.get_strength() >= self.maximum:
				player.message('Voce ja esta com o maximo de pontos forca!')
				return True
			if player.get_strength() + points > self.maximum:
				points = self.maximum - player.get_strength()
			if player.get_points() < points:
				player.message('[Sistema] Voce nao possui esses pontos!')
				return True
			player.set_strength(player.get_strength() + points)
			player.set_points(player.get_points() - points)
			player.message('[Sistema] Pontos adicionados!')
			player.refresh()
		return True

	#	
	# Dexterity
	#
	def add_dexterity(self, player, arguments):
		if len(arguments) != 1:
			player.message('[Sistema] Uso: /a <pontos>')
		else:
			points = int(arguments[0])
			if player.get_dexterity() >= self.maximum:
				player.message('[Sistema] Voce ja esta com o maximo de pontos em agilidade!')
				return True
			if player.get_dexterity() + points > self.maximum:
				points = self.maximum - player.get_dexterity()
			if player.get_points() < points:
				player.message('[Sistema] Voce nao possui esses pontos!')
				return True
			player.set_dexterity(player.get_dexterity() + points)
			player.set_points(player.get_points() - points)
			player.message('[Sistema] Pontos adicionados!')
			player.refresh()
		return True

	#	
	# Vitality
	#
	def add_vitality(self, player, arguments):
		if len(arguments) != 1:
			player.message('Uso: /v <pontos>')
		else:
			points = int(arguments[0])
			if player.get_vitality() >= self.maximum:
				player.message('[Sistema] Voce ja esta com o maximo de pontos em vitalidade!')
				return True
			if player.get_vitality() + points > self.maximum:
				points = self.maximum - player.get_vitality()
			if player.get_points() < points:
				player.message('[Sistema] Voce nao possui esses pontos!')
				return True
			player.set_vitality(player.get_vitality() + points)
			player.set_points(player.get_points() - points)
			player.message('[Sistema] Pontos adicionados!')
			player.refresh()
		return True

	#	
	# Energy
	#
	def add_energy(self, player, arguments):
		if len(arguments) != 1:
			player.message('[Sistema] Uso: /e <pontos>')
		else:
			points = int(arguments[0])
			if player.get_energy() >= self.maximum:
				player.message('[Sistema] Voce ja esta com o maximo de pontos em energia!')
				return True
			if player.get_energy() + points > self.maximum:
				points = self.maximum - player.get_energy()
			if player.get_points() < points:
				player.message('[Sistema] Voce nao possui esses pontos!')
				return True
			player.set_energy(player.get_energy() + points)
			player.set_points(player.get_points() - points)
			player.message('[Sistema] Pontos adicionados!')
			player.refresh()
		return True
	
	#
	# Manual
	#
	def add_point(self, index, where):
		player = Player(index)
		if where == 0: # Strength
			if player.get_strength() >= self.maximum:
				player.message('[Sistema] Voce ja atingiu o maximo de pontos!')
				return False
		elif where == 1: # Dexterity
			if player.get_dexterity() >= self.maximum:
				player.message('[Sistema] Voce ja atingiu o maximo de pontos!')
				return False
		elif where == 2: # Vitality
			if player.get_vitality() >= self.maximum:
				player.message('[Sistema] Voce ja atingiu o maximo de pontos!')
				return False
		elif where == 3: # Energy
			if player.get_energy() >= self.maximum:
				player.message('[Sistema] Voce ja atingiu o maximo de pontos!')
				return False
		else:
			return False
		return True

#
# Initialization
#
commands.register(StatusCommand())
