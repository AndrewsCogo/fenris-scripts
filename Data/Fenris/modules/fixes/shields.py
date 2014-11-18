#
# Imports
#
from wolfulus import *
from ..util.player import *

# 
# Character calculation
#
def character_calc(index):
	player = Player(index)
	inventory = player.get_inventory()
	if not inventory.has_item(1): 
		return
	item = inventory.get_item(1)
	if item.get_section() != 6:
		return
	if not (item.get_index() >= 17 and item.get_index() <= 31):
		return
	if not item.is_excellent():
		return
	if item.has_life():
		antes = player.get_addlife()
		depois = player.get_addlife() + (player.get_maxlife() * 4 / 100)
		player.set_addlife(int(depois) & 0xFFFF)
	if item.has_mana():
		antes = player.get_addmana()
		depois = player.get_addmana() + (player.get_maxmana() * 4 / 100)
		player.set_addmana(int(depois) & 0xFFFF)
	player.refill()

#
# Custom character calculation
#
Events.register('player.set', character_calc)