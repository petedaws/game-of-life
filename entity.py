import subprocess
import socket
import time
import event
import random
import sys
import conf

class Entity(event.Event):

	def __init__(self,entity_id,pos_x,pos_y,factor):
		event.Event.__init__(self)
		self.entity_id = entity_id
		self.position = (int(pos_x),int(pos_y))
		self.move_factor = int(factor)
		self.connect('position_update',self.update_tx)

	def move(self):
		new_x = random.randrange(-1,2)*self.move_factor
		new_y = random.randrange(-1,2)*self.move_factor
		self.position = (self.position[0]+new_x,self.position[1]+new_y)
		data = {
			'entity_id':self.entity_id,
			'position':self.position,
			}
		self.emit('position_update',data)

	def update_tx(self,data):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.sendto(str(data), (conf.message_bus_grp, conf.message_bus_port))


def run(entity_id,pos_x,pos_y,factor):
	entity = Entity(entity_id,pos_x,pos_y,factor)
	event.add_timer(0.1,entity.move,name='timer1')
	event.mainloop()

if __name__ == "__main__":
	run(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
