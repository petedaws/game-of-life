import subprocess
import messagebus
import time
import event
import random
import sys
import conf

class Entity(event.Event):

	def __init__(self,init_attributes):
		event.Event.__init__(self)
		self.message_rx = messagebus.MessageRx()
		self.message_tx = messagebus.MessageTx()
		self.other_entities = {}
		self.__init_attributes(init_attributes)
		event.add_io_watcher(self.message_rx.sock,self.message_rx.receive)

	def __init_attributes(self,init_attributes):
		self.entity_id,attributes = init_attributes.iteritems().next()
		if messagebus.validate_attributes(attributes):
			self.attributes = attributes

	def update_tx(self):
		self.message_tx.transmit({self.entity_id:self.attributes})

	def behaviour_random(self):
		new_x = random.randrange(-1,2)
		new_y = random.randrange(-1,2)
		self.attributes['position_x'] = self.attributes['position_x']+new_x
		self.attributes['position_y'] = self.attributes['position_y']+new_y
		self.emit('update')

	def behaviour_avoid(self):
		for entity_id in self.other_entities:
			x_dist = self.other_entities[entity_id].attributes['position_x'] - self.attributes['position_x']
			y_dist = self.other_entities[entity_id].attributes['position_y'] - self.attributes['position_y']
			if abs(x_dist) < 50:
				self.attributes['position_x'] = self.attributes['position_x'] + 2
			if abs(y_dist) < 50:
				self.attributes['position_y'] = self.attributes['position_y'] + 2
		self.emit('update')

	def observe_other_entity(self,entity_message):	
		entity_id,attributes = entity_message.popitem()
		
		if entity_id == self.entity_id:
			return
		if entity_id in self.other_entities:
			self.other_entities[entity_id].attributes.update(attributes)
		else:
			self.other_entities[entity_id] = Entity({entity_id:attributes})

def run(entity_id,behaviour,init_attributes):
	entity = Entity({entity_id:init_attributes})
	entity.connect('update',entity.update_tx)
	entity.connect('new_message',entity.observe_other_entity)
	if behaviour == 1:
		event.add_timer(0.1,entity.behaviour_random,name='timer1')
	else:
		event.add_timer(0.1,entity.behaviour_avoid,name='timer1')
	event.mainloop()

if __name__ == "__main__":

	test_init =   {
			'position_x':100,
			'position_y':100,
			'type':'grass',
			'state':'alive',
			'age':0,
			'max_age':20,
			'food':5,
			'reproduce_food':50,
			'max_speed':5.0,
			}

	run(int(sys.argv[1]),int(sys.argv[2]),test_init)
