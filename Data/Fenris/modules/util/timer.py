#
# Imports
#

from wolfulus import *
import math

#
# Timer class
#
class Timer(object):

	# Constructor
	def __init__(self, callback, step, count):
		self.callback = callback
		self.current = 0
		self.last = 0
		self.count = count
		self.step = step
		return
#
# Timer manager
#
class TimerManager(object):

	# Constructor
	def __init__(self):
		Events.register('timer.tick', self.tick)
		self.timers = dict()
		self.id = 0
		return

	# Resets all timers
	def reset(self):
		self.timers = dict()
		return

	# Clears a timer
	def clear(self, index):
		if self.timers.has_key(index):
			del self.timers[index]
		return

	# Timeout timers
	def timeout(self, callback, step):
		id = self.id + 1
		self.id = id
		self.timers[id] = Timer(callback, step, -1)
		return id

	# Interval timers
	def interval(self, callback, step):
		id = self.id + 1
		self.id = id
		self.timers[id] = Timer(callback, step, 0)
		return id

	# Repeat timers
	def repeat(self, callback, step, count):
		id = self.id + 1
		self.id = id
		self.timers[id] = Timer(callback, step, 1 + count)
		return id

	# Tick event
	def tick(self, ms):
		for index in self.timers.keys():
			timer = self.timers[index]
			timer.current = timer.current + ms
			if timer.current - timer.last >= timer.step:
				count = math.floor((timer.current - timer.last) / timer.step)
				remainder = (timer.current - timer.last) % timer.step
				timer.last = timer.current - remainder
				self.timers[index] = timer
				if self.timers[index].count < 0: # Timeout
					self.timers[index].callback()
					self.clear(index)
				elif self.timers[index].count == 0: # Interval
					while count > 0 and self.timers.has_key(index):
						self.timers[index].callback()
						count = count - 1
				elif self.timers[index].count > 1: # Repeats
					while count > 0 and self.timers.has_key(index):
						self.timers[index].callback()
						self.timers[index].count = self.timers[index].count - 1
						if self.timers[index].count == 1:
							self.clear(index)
							break
						count = count - 1
				else:
					self.clear(index)
		return

#
# Timer 
#
timer = TimerManager()