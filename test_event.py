import socket
import time
import event
import struct

class TimerTest(event.Event):
	
	def __init__(self,hellostring='helloworld'):
		self.hellostring = hellostring

	def hello(self):
		print '%s: %f' % (self.hellostring,time.time())

class SocketTest(event.Event):
	
	def __init__(self,port=10000):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', port))
		mreq = struct.pack("4sl", socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def receive(self):
		data = self.sock.recv(1024)
		print data

def main():

	timer1 = TimerTest('timer2')
	timer2 = TimerTest('timer1')
	sock1 = SocketTest(10001)
	sock2 = SocketTest(10002)

	event.add_timer(1,timer1.hello)
	event.add_timer(3,timer2.hello)
	event.add_io_watcher(sock1.sock,sock1.receive)
	event.add_io_watcher(sock2.sock,sock2.receive)

	event.mainloop()

main()
