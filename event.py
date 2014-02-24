import socket
import select
import time 
import pprint

class Event:

	def __init__(self):
		self.timers = []

	def emit(self,event_name,*args):
		for event in events:
			if event['name'] == event_name:
				event['callback'](*args)

	def connect(self,event_name,callback):
		assert callable(callback)
		events.append({'name':event_name,'callback':callback})

	def timer_add(self,event_name,period):
		self.timers.append[(event_name,period)]

	def run(self):
		pass

events = []
timers = []
read_fds = {}
write_fds = []

def add_timer(interval,callback,name=''):
	next = time.time() + interval
	timers.append({'name':name,'interval':interval,'callback':callback})

def modify_timer(name,interval=None,callback=None):
	for timer in timers:
		if timer['name'] == name:
			if interval is not None:
				timer['interval'] = interval
			if callback is not None:
				timer['callback'] = callback
	

def add_io_watcher(fd,callback):
	read_fds[fd] = callback

def mainloop():
	
	for timer in timers:
		timer['next'] = time.time() + timer['interval']

	while True:
		next_timer = None
		timeout = None
		for timer in timers:
			if timer['interval'] == 0:
				continue
			if next_timer is None or timer['next'] < next_timer['next']:
				next_timer = timer
				timeout = next_timer['next'] - time.time()

		readable, writeable, exceptional = select.select(read_fds.keys(), write_fds, read_fds,max(timeout,0))

		for timer in timers:
			if timer['interval'] == 0:
				continue
			if timer['next'] - time.time() <= 0:
				timer['callback']()
				timer['next'] = time.time() + timer['interval']

		if len(readable):
			for reader in readable:
				for read_fd in read_fds.keys():
					if read_fd is reader:
						read_fds[read_fd]()
