#
# Imports
#
from wolfulus import *
from ..util.player import *

#
# Handler class
#
def entrou(index):
	# ignora os monstros
	if index < Server.player_start: 
		return
	player = Player(index)
	Server.send_message_all('%s entrou no jogo!' % player.get_name())

# Chama a funcao entrou toda vez que um jogador entrar no jogo
Events.register('player.join', entrou)