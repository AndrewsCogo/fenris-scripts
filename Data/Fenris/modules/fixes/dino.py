#
# Imports
#
from wolfulus import *

#
# Durabilidade ilimitada para pets (v97d)
#
Memory.write_uint8(0x00465B27, 0x90)
Memory.write_uint8(0x00465B28, 0x90)