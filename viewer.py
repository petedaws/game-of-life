import sys
#import and init pygame
import pygame
import conf
import socket
import event

pygame.init() 

#create the screen
window = pygame.display.set_mode((640, 480)) 

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

class circle:
	def __init__(self,init_pos):
		self.circle_pos = init_pos

	def move(self):
		self.circle_pos = (self.circle_pos[0]+3,self.circle_pos[1])
		window.fill(RED)
		pygame.draw.circle(window,BLUE,self.circle_pos,5)
		pygame.display.flip() 

window.fill(RED)

c = circle((0,5))

event.add_timer(0.2,c.move)

event.mainloop()

