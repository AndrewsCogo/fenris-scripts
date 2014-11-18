#
# Imports
#

from wolfulus import *
from item import *

#
# Inventory class
#
class Inventory(object):

	# Constructor
	def __init__(self, address):
		self.offset = address
		
	# Gets a variable address
	def get_address(self, variable):
		addr = self.offset + variable
		return addr
	
	# Gets an item
	def get_item(self, position):
		if (position >= 0 and position < 76):
			return Item(self.offset + (position * 0x84), position)
		return False

	# Checks if there's an item on the specified position
	def has_item(self, position):
		if (position >= 0 and position < 76):
			item = Item(self.offset + (position * 0x84), position)
			if (item.is_valid()):
				return item
		return False
	
	# Gets all items
	def get_items(self):
		lst = []
		for i in range(76):
			item = Item(self.offset + (position * 0x84), i)
			if (item.is_valid()):
				lst.append(item)
		return lst

	# Gets all items
	def find(self, section, index, level = -1):
		for i in range(76):
			if self.has_item(i):
				item = self.get_item(i)
				if item.is_item(section, index):
					if level == -1:
						return item
					else:
						if item.get_level() == level:
							return item
		return False