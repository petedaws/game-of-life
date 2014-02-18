import subprocess
import socket
import time

import conf

class cell:

	def __init__(self):
		self.cell_id = '1'
		self.position = (0,0)
		self.alive()

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
