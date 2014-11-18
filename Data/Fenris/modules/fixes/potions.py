#
# Imports
#
from wolfulus import *

#
# Durabilidade ilimitada para potions (v97d)
#
Memory.write_uint8(0x00427EE8, 0)
Memory.write_uint8(0x00428167, 0)