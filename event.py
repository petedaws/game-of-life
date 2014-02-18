import socket
import select

class Event:

	def __init__(self):
		self.events = {}
		self.timers = []

	def emit(self,event):
		self.events[event]()

	def connect(self,event_name,callback):
		assert callable(callback)
		self.events[event] = callback

	def timer_add(self,event_name,period)
		self.timers.append[(event_name,period)]

	def run(self):
		pass

		

		
if __name__ == "__main__":

	def test():
		print 'test_event'

	e = Event()
	e.connect('test',test)
	e.emit('test')
	e.run()
