import sys
import pygame
import conf
import socket
import event
import messagebus
import struct
import behaviour

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

COLOUR_MAP = {'RandomMove':BLUE, 'Avoid':GREEN}
		

class CellModel():
	def __init__(self,init_pos_x,init_pos_y,color):
		self.pos_x = int(init_pos_x)
		self.pos_y = int(init_pos_y)
		self.color = color

	def update(self,pos_x,pos_y):
		self.pos_x = int(pos_x)
		self.pos_y = int(pos_y)

	def draw(self,window):
		pygame.draw.circle(window,self.color,(self.pos_x,self.pos_y),5)

class Viewer(event.Event):
	
	def __init__(self):
		event.Event.__init__(self)
		pygame.init() 
		self.window = pygame.display.set_mode((640, 480)) 
		self.centre = [320,240]
		self.scroll = [0,0]
		self.pos_prev = [0,0]
		self.entities = {}
		self.message_rx = messagebus.MessageRx()
		self.message_rx.connect('new_message',self.process_entity)

	def start(self):
		event.add_timer(0.02,self.draw)
		event.add_io_watcher(self.message_rx.sock,self.message_rx.receive)
		event.mainloop()

	def process_entity(self,message):
		for entity_id,attributes in message.iteritems():
			if entity_id in self.entities:
				self.entities[entity_id].update(attributes['position_x']+self.centre[0],attributes['position_y']+self.centre[1])
			else:
				self.entities[entity_id] = CellModel(attributes['position_x']+self.centre[0],attributes['position_y']+self.centre[1],COLOUR_MAP[attributes['behaviour']])
			if attributes['state'] == 'dead':
				del self.entities[entity_id]

	def draw_entities(self):
		for entity in self.entities:
			self.entities[entity].draw(self.window)

	def draw(self):
		self.window.fill(RED)
		self.draw_entities()
		self.scroll_screen()
		pygame.display.flip()

	def scroll_screen(self):
		e = pygame.event.poll()
		if e.type == pygame.MOUSEMOTION:
			if pygame.mouse.get_pressed()[0]:
				if self.pos_prev is None:
					self.pos_prev = [e.pos[0],e.pos[1]]
				else:
					self.scroll = [e.pos[0] - self.pos_prev[0],e.pos[1] - self.pos_prev[1]]
					self.pos_prev = [e.pos[0],e.pos[1]]
					self.centre = [self.centre[0] + self.scroll[0],self.centre[1] + self.scroll[1]]
			else:
				self.pos_prev = None					
		pygame.event.clear()

if __name__ == "__main__":
	viewer = Viewer()
	viewer.start()




