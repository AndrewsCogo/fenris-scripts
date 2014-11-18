#
# Imports
#

from wolfulus import *
from inventory import * 
from item import * 
import database
import struct

#
# Player class
#
class Player(object):
	
	# Constants
	PLAYER_EMPTY = 0
	PLAYER_CONNECTED = 1
	PLAYER_LOGGED = 2	
	PLAYER_PLAYING = 3

	# Constructor
	def __init__(self, index):
		self.index = index
		self.offset = Server.object_address(index)
	
	# Gets the player index
	def get_index(self):
		return self.index
		
	# Gets a variable address
	def get_address(self, variable):
		addr = self.offset + variable
		return addr

	# Gets the player name
	def get_name(self):
		return Memory.read_string(self.get_address(0x6A), 10)

	# Gets the player account
	def get_account(self):
		return Memory.read_string(self.get_address(0x5F), 10)

	# Strength
	def get_strength(self):
		return Memory.read_uint16(self.get_address(0x98))
	def set_strength(self, val):
		return Memory.write_uint16(self.get_address(0x98), val)

	# Dexterity
	def get_dexterity(self):
		return Memory.read_uint16(self.get_address(0x9A))
	def set_dexterity(self, val):
		return Memory.write_uint16(self.get_address(0x9A), val)

	# Vitality
	def get_vitality(self):
		return Memory.read_uint16(self.get_address(0x9C))
	def set_vitality(self, val):
		return Memory.write_uint16(self.get_address(0x9C), val)

	# Energy
	def get_energy(self):
		return Memory.read_uint16(self.get_address(0x9E))
	def set_energy(self, val):
		return Memory.write_uint16(self.get_address(0x9E), val)

	# Points
	def get_points(self):
		return Memory.read_uint32(self.get_address(0x88))
	def set_points(self, val):
		Memory.write_uint32(self.get_address(0x88), val)

	# AddMana
	def get_addmana(self):
		return Memory.read_uint16(self.get_address(0xDC))
	def set_addmana(self, val):
		Memory.write_uint16(self.get_address(0xDC), val)

	# AddLife
	def get_addlife(self):
		return Memory.read_uint16(self.get_address(0xDA))
	def set_addlife(self, val):
		Memory.write_uint16(self.get_address(0xDA), val)

	# AddBP
	def get_addbp(self):
		return Memory.read_uint32(self.get_address(0xC0))
	def set_addbp(self, val):
		Memory.write_uint32(self.get_address(0xC0), val)

	# AddBP
	def get_maxbp(self):
		return Memory.read_uint32(self.get_address(0xBC))
	def set_maxbp(self, val):
		Memory.write_uint32(self.get_address(0xBC), val)

	# BP
	def get_bp(self):
		return Memory.read_uint32(self.get_address(0xB8))
	def set_bp(self, val):
		Memory.write_uint32(self.get_address(0xB8), val)

	# Life
	def get_life(self):
		return Memory.read_float(self.get_address(0xA0))
	def set_bp(self, val):
		Memory.write_float(self.get_address(0xA0), val)

	# MaxLife
	def get_maxlife(self):
		return Memory.read_float(self.get_address(0xA4))
	def set_bp(self, val):
		Memory.read_float(self.get_address(0xA4), val)

	# Mana
	def get_mana(self):
		return Memory.read_float(self.get_address(0xB0))
	def set_mana(self, val):
		Memory.read_float(self.get_address(0xB0), val)

	# MaxMana
	def get_maxmana(self):
		return Memory.read_float(self.get_address(0xB4))
	def set_maxmana(self, val):
		Memory.read_float(self.get_address(0xB4), val)

	# FillLife
	def get_filllife(self):
		return Memory.read_float(self.get_address(0xA8))
	def set_filllife(self, val):
		Memory.read_float(self.get_address(0xA8), val)

	# FillLifeMax
	def get_filllifemax(self):
		return Memory.read_float(self.get_address(0xAC))
	def set_filllifemax(self, val):
		Memory.read_float(self.get_address(0xAC), val)

	# Gets the player authority
	def get_authority(self):
		return Memory.read_uint32(self.get_address(0x170))
		
	# Gets the player authority code
	def get_authority_code(self):
		return Memory.read_uint32(self.get_address(0x174))
		
	# Gets the player skin
	def get_skin(self):
		return Memory.read_int32(self.get_address(0x27C))
				
	# Gets the player skin
	def set_skin(self, skin):
		ret = Memory.write_int32(self.get_address(0x27C), skin)	
		self.refresh()
		return ret

	# Gets the player close type
	def get_closetype(self):
		return Memory.read_uint8(self.get_address(0x0B))
	def set_closetype(self, value):
		return Memory.write_uint8(self.get_address(0x0B), value)

	# Gets the player close count
	def get_closecount(self):
		return Memory.read_uint8(self.get_address(0x0A))
	def set_closecount(self, value):
		return Memory.write_uint8(self.get_address(0x0A), value)
		
	# Gets the player level
	def get_level(self):
		return Memory.read_uint16(self.get_address(0x86))
	def set_level(self, val):
		return Memory.write_uint16(self.get_address(0x86), val)

	# Gets the player exp
	def get_exp(self):
		return Memory.read_uint32(self.get_address(0x8C))
	def set_exp(self, val):
		return Memory.write_uint32(self.get_address(0x8C), val)

	# Gets the player map number
	def get_map(self):
		return Memory.read_uint8(self.get_address(0xD9))
	def set_map(self, value):
		return Memory.write_uint8(self.get_address(0xD9), value)
		
	# Gets the player position x
	def get_x(self):
		return Memory.read_uint16(self.get_address(0xD4))
	def set_x(self, value):
		return Memory.write_uint16(self.get_address(0xD4), value)
		
	# Gets the player position y
	def get_y(self):
		return Memory.read_uint16(self.get_address(0xD6))
	def set_y(self, value):
		return Memory.write_uint16(self.get_address(0xD6), value)

	# Gets the player pk level
	def get_pklevel(self):
		return Memory.read_uint8(self.get_address(0xCD))
	def set_pklevel(self, value):
		ret = Memory.write_uint8(self.get_address(0xCD), value)
		pkt = struct.pack('BBBBBBB', 0xC1, 0x07, 0xF3, 0x08, (self.get_index() >> 8) & 0xFF, self.get_index() & 0xFF, value & 0xFF)
		for p in self.get_near_players():
			Server.send_packet(p, pkt, len(pkt))
		self.packet(pkt)
		return ret

	# Gets the player pk count
	def get_pkcount(self):
		return Memory.read_uint8(self.get_address(0xCC))
	def set_pkcount(self, value):
		return Memory.write_uint8(self.get_address(0xCC), value)

	# Gets the player pk time
	def get_pktime(self):
		return Memory.read_uint32(self.get_address(0xD0))
	def set_pktime(self, value):
		return Memory.write_uint32(self.get_address(0xD0), value)

	# Gets the inventory
	def get_inventory(self):
		return Inventory(Memory.read_uint32(self.get_address(0xC24)))

	# Money
	def get_money(self):
		return Memory.read_uin32(self.get_address(0x94))
	def set_money(self, value):
		ret = Memory.write_uint32(self.get_address(0x94), value)
		self.packet(struct.pack('BBBBBBBB', 0xC3, 0x08, 0x22, 0xFE, (value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF))
		return ret

	# Gets a list of all the near players
	def get_near_players(self):
		objs = []
		base = self.get_address(0x32C)
		for i in range(75):
			vp = base + (0x0C * i)
			state = Memory.read_uint8(vp)
			number = Memory.read_uint16(vp + 2)
			type = Memory.read_uint8(vp + 4)
			if (state == 1 or state == 2) and type == 1: # user
				if number >= 0 and number < Server.object_max: # range
					objs.append(number)
		return objs

	# Gets a list of all the near monsters
	def get_near_monsters(self):
		objs = []
		base = self.get_address(0x32C)
		for i in range(75):
			vp = base + (0x0C * i)
			state = Memory.read_uint8(vp)
			number = Memory.read_uint16(vp + 2)
			type = Memory.read_uint8(vp + 4)
			if (state == 1 or state == 2) and (type == 2 or type == 3): # monster
				if number >= 0 and number < Server.object_max: # range
					objs.append(number)
		return objs

	# Resets
	def get_resets(self):
		db = database.get('muonline')
		cursor = db.cursor()
		cursor.execute("SELECT Resets FROM Character WHERE Name = ?", [self.get_name()])
		character = cursor.fetchone()
		if not character:
			return -1
		else:
			return character.Resets
	
	# Resets
	def set_resets(self, value):
		db = database.get('muonline')
		cursor = db.cursor()
		cursor.execute("UPDATE Character SET Resets = ? WHERE Name = ?", [value, self.get_name()])
		db.commit()

	# Resets
	def increment_resets(self):
		db = database.get('muonline')
		db.cursor().execute("UPDATE Character SET Resets = Resets + 1 WHERE Name = ?", [self.get_name()])
		db.commit()

	# Check if user is vip
	def is_vip(self):
		db = database.get('muonline')
		cursor = db.cursor()
		cursor.execute("SELECT vip FROM MEMB_INFO WHERE memb___id = ?", [self.get_account()])
		acc = cursor.fetchone()
		if not acc:
			return False
		else:
			if acc.vip > 0:
				return True
			else:
				return False

	# Checks if player is admin
	def is_admin(self):
		return self.get_authority() & 2 == 2

	# Check if connected
	def is_connected(self):
		return Memory.read_int32(self.get_address(0x04)) >= self.PLAYER_CONNECTED
	
	# Check if logged
	def is_loggedin(self):
		return Memory.read_int32(self.get_address(0x04)) >= self.PLAYER_LOGGED
		
	# Check if connected
	def is_playing(self):
		return Memory.read_int32(self.get_address(0x04)) >= self.PLAYER_PLAYING
			
	# Teleports the character
	def teleport(self, map, x, y):
		Server.teleport(self.index, map, x, y)
		return
		
	# Disconnects the current player
	def disconnect(self):		
		Server.disconnect(self.index)
		return
		
	# Sends a message
	def announce(self, msg): 
		Server.send_announcement(self.index, msg)
		return
		
	# Sends a message
	def message(self, msg):
		Server.send_message(self.index, msg)
		return

	# Refreshes the player on the screen
	def refresh(self):
		Server.refresh(self.get_index(), self.get_map(), self.get_x(), self.get_y())
		return

	# Refreshes the player on the screen
	def refill(self):
		Server.refill(self.get_index())
		return

	# Sends a packet
	def packet(self, packet):
		Server.send_packet(self.get_index(), packet, len(packet))
		return 

	# Character selection
	def select_character(self):
		self.set_closecount(1)
		self.set_closetype(1)