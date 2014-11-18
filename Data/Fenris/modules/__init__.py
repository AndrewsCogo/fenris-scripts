#
# Nao modificar
#
import os
import glob

from commands import *
from fixes import *

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/[!_]*.py")]