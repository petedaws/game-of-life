import subprocess
import socket
import time
from event import Event

import conf

class cell(Event):

	def __init__(self):
		self.cell_id = '1'
		self.position = (0,0)
		self.setup_listener()
		self.connect('rx',self.process_rx)
		self.connect('report',self.report)
		self.timer_add('report')
		self.alive()


	def run_listener(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', conf.cell_port))
		mreq = struct.pack("4sl", socket.inet_aton(conf.MCAST_GRP), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		while True:
			for sock in readable:
				 sock.recv(1024)

	def process_rx(self):


	def report(self):
		data = {
			'cell_id':self.cell_id,
			'position':self.position,
			}

		MCAST_GRP = '224.1.1.1'
		MCAST_PORT = 5007

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.sendto(str(data), (conf.MCAST_GRP, conf.MCAST_PORT))
		print "sent data to %s" % (str((conf.MCAST_GRP, conf.MCAST_PORT)))

	def alive(self):
		
		while(1):
			self.report()
			time.sleep(1)

if __name__ == "__main__":
	cell()
