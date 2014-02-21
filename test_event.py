import socket
import time
import event
import struct

class TimerTest(event.Event):
	
	def __init__(self,hellostring='helloworld'):
		event.Event.__init__(self)
		self.hellostring = hellostring

	def hello(self):
		print '%s: %f' % (self.hellostring,time.time())

	def stop(self,timer_name):
		print 'stopping timer: %s' % timer_name
		event.modify_timer(timer_name,interval=0)

	def modify_timer(self,timer_name,new_interval):
		print 'modify timer: %s' % timer_name
		event.modify_timer(timer_name,new_interval)

class SocketTest(event.Event):
	
	def __init__(self,port=10000):
		event.Event.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', port))
		mreq = struct.pack("4sl", socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def receive(self):
		message = self.sock.recv(1024)
		if message == 'execute':
			self.emit('test',message)
		if message.split('_')[0] == 'stop':
			self.emit('stop',message.split('_')[1])
		if message.split('_')[0] == 'modifytimer':
			self.emit('modifytimer',message.split('_')[1],float(message.split('_')[2]))
			
	def send(self,message=''):
		print 'socket send: %s' % message

def main():

	timer1 = TimerTest('timer1')
	timer2 = TimerTest('timer2')
	sock1 = SocketTest(10001)
	sock2 = SocketTest(10002)

	sock1.connect('test',sock2.send)
	sock1.connect('stop',timer1.stop)
	sock1.connect('stop',timer2.stop)
	sock1.connect('modifytimer',timer1.modify_timer)
	sock1.connect('modifytimer',timer2.modify_timer)
	event.add_timer(1,timer1.hello,name='timer1')
	event.add_timer(3,timer2.hello,name='timer2')
	event.add_io_watcher(sock1.sock,sock1.receive)
	event.add_io_watcher(sock2.sock,sock2.receive)

	event.mainloop()

main()
