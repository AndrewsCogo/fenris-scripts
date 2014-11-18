import scheduler
from ..util.timer import *
import time

def evento():
	Console.log('Eu vou acontecer todo sabado as 2 da tarde')

sc = scheduler.Scheduler()
sc.every().saturday.at('14:00').do(evento)
timer.interval(sc.run_pending, 250)