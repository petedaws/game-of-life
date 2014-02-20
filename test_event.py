import socket
import time
import event
import struct

class TimerTest(event.Event):
	
	def hello(self):
		print 'helloworld: %f' % time.time()

class SocketTest(event.Event):
	
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', 30010))
		mreq = struct.pack("4sl", socket.inet_aton('224.1.1.1'), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def receive(self):
		data = self.sock.recv(1024)
		print data

def main():

	testTimer = TimerTest()
	testSocket = SocketTest()

	event.add_timer(2,testTimer.hello)
	event.add_io_watcher(testSocket.sock,testSocket.receive)

	event.mainloop()

main()
