import sys
#import and init pygame
import pygame
import conf
import socket
import event
import struct

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

class Message(event.Event):
	
	def __init__(self,port=10000):
		event.Event.__init__(self)
		self.__create_socket()
		self.connect('new_message',self.process)

	def __create_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', conf.message_bus_port))
		mreq = struct.pack("4sl", socket.inet_aton(conf.message_bus_grp), socket.INADDR_ANY)
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

	def receive(self):
		message = self.sock.recv(1024)
		self.emit('new_message',message)

	def process(self,message):
		packet = eval(message)
		if 'entity_id' in packet:
			self.emit('entity_update',packet)
		

class CellModel():
	def __init__(self,init_pos):
		self.pos = init_pos

	def update(self,pos):
		self.pos = pos

	def draw(self,window):
		pygame.draw.circle(window,BLUE,self.pos,5)

class Viewer(event.Event):
	
	def __init__(self):
		event.Event.__init__(self)
		pygame.init() 
		self.window = pygame.display.set_mode((640, 480)) 
		self.entities = {}
		self.messager = Message()
		self.connect('entity_update',self.process_entity)

	def start(self):
		event.add_timer(0.02,self.draw)
		event.add_io_watcher(self.messager.sock,self.messager.receive)
		event.mainloop()

	def process_entity(self,entity_message):
		if entity_message['entity_id'] in self.entities:
			self.entities[entity_message['entity_id']].update(entity_message['position'])
		else:
			self.entities[entity_message['entity_id']] = CellModel(entity_message['position'])

	def draw_entities(self):
		for entity in self.entities:
			self.entities[entity].draw(self.window)

	def draw(self):
		self.window.fill(RED)
		self.draw_entities()
		pygame.display.flip()

if __name__ == "__main__":
	viewer = Viewer()
	viewer.start()




