#
# Imports
#
from wolfulus import *
from modules import *
from modules.util import database
from modules.util import log

# 
# Main
#
def main():
	database.set('muonline', Settings.read('global.database').as_string("def"))
	return
	