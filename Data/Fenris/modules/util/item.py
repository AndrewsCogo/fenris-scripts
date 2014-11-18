#
# Imports
#

from wolfulus import *

#
# Item class
#
class Item(object):

	# Constructor
	def __init__(self, address, position = -1):
		self.position = position
		self.offset = address
		
	# Gets a variable address
	def get_address(self, variable):
		addr = self.offset + variable
		return addr

	# Position
	def get_position(self):
		return self.position
	
	# Type 

	def get_type(self):
		return Memory.read_uint16(self.get_address(0x06))
	def set_type(self, type):
		Memory.write_uint16(self.get_address(0x06), type)
		
	# Section
	def get_section(self):
		return self.get_type() / 32
	
	def get_index(self):
		return self.get_type() % 32
	
	def set(self, section, index):
		self.set_type((section * 32) + index)

	# Checks 

	def is_valid(self):
		return self.get_type() != 0xFFFF
	
	def is_item(self, section, index):
		return self.get_section() == section and self.get_index() == index

	# Level
	
	def get_level(self):
		return Memory.read_uint16(self.get_address(0x08))

	def set_level(self, level):
		Memory.write_uint16(self.get_address(0x08), level)

	# Durability

	def get_durability(self):
		return Memory.read_float(self.get_address(0x24))

	def set_durability(self, durability):
		Memory.write_float(self.get_address(0x24), durability)
	
	# Excellents

	def get_excellent(self):
		return Memory.read_uint8(self.get_address(0x6B))

	def set_excellent(self, excellent):
		Memory.write_uint8(self.get_address(0x6B), excellent)

	def is_excellent(self):
		return (self.get_excellent() & 0x7F) != 0

	def has_life(self):
		return (self.get_excellent() & 32) != 0
	
	def has_mana(self):
		return (self.get_excellent() & 16) != 0
	
	def has_defense(self):
		return (self.get_excellent() & 8) != 0
	
	def has_reflect(self):
		return (self.get_excellent() & 4) != 0

	def has_defenserate(self):
		return (self.get_excellent() & 2) != 0
	
	def has_money(self):
		return (self.get_excellent() & 1) != 0
	
	def has_damage(self):
		return (self.get_excellent() & 32) != 0
	
	def has_attackrate(self):
		return (self.get_excellent() & 16) != 0
	
	def has_attackrate2(self):
		return (self.get_excellent() & 8) != 0
	
	def has_attackspeed(self):
		return (self.get_excellent() & 4) != 0
	
	def has_liferegen(self):
		return (self.get_excellent() & 2) != 0
	
	def has_manaregen(self):
		return (self.get_excellent() & 1) != 0

	# Skill
	
	def has_skill(self):
		return Memory.read_uint8(self.get_address(0x68)) != 0
	
	def set_skill(self, skill):
		Memory.write_uint8(self.get_address(0x68), 1 if skill else 0)
	
	# Luck

	def has_luck(self):
		return Memory.read_uint8(self.get_address(0x69)) != 0
	
	def set_luck(self, luck):
		Memory.write_uint8(self.get_address(0x69), 1 if luck else 0)
	
	# Option

	def get_option(self):
		return Memory.read_uint8(self.get_address(0x6A)) != 0
	
	def set_option(self, option):
		Memory.write_uint8(self.get_address(0x6A), option)

