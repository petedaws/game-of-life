import socket
import select
import time 

class Event:

	def __init__(self):
		self.events = {}
		self.timers = []

	def emit(self,event):
		self.events[event]()

	def connect(self,event_name,callback):
		assert callable(callback)
		self.events[event] = callback

	def timer_add(self,event_name,period):
		self.timers.append[(event_name,period)]

	def run(self):
		pass


timers = []
read_fds = {}
write_fds = []

def add_timer(interval,callback):
	next = time.time() + interval
	timers.append({'interval':interval,'callback':callback})

def add_io_watcher(fd,callback):
	read_fds[fd] = callback

def mainloop():
	
	for timer in timers:
		timer['next'] = time.time() + timer['interval']

	while True:
		next_timer = None
		timeout = None
		for timer in timers:
			if next_timer is None or timer['next'] < next_timer['next']:
				next_timer = timer
				timeout = next_timer['next'] - time.time()

		readable, writeable, exceptional = select.select(read_fds.keys(), write_fds, read_fds,max(timeout,0))

		for timer in timers:
			if timer['next'] - time.time() <= 0:
				timer['callback']()
				timer['next'] = time.time() + timer['interval']

		if len(readable):
			for reader in readable:
				for read_fd in read_fds.keys():
					if read_fd is reader:
						read_fds[read_fd]()
			
		
if __name__ == "__main__":

	def test():
		print 'test_event'

	e = Event()
	e.connect('test',test)
	e.emit('test')
	e.run()
