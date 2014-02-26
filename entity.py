import subprocess
import messagebus
import time
import event
import sys
import conf
from behaviour import *

class Entity(event.Event):

	def __init__(self,init_attributes):
		event.Event.__init__(self)
		self.message_rx = messagebus.MessageRx()
		self.message_tx = messagebus.MessageTx()
		self.other_entities = {}
		self.__init_attributes(init_attributes)
		behav = eval(self.attributes['behaviour'])(self)
		self.behaviour = behav
		event.add_io_watcher(self.message_rx.sock,self.message_rx.receive)


	def __init_attributes(self,init_attributes):
		self.entity_id,attributes = init_attributes.iteritems().next()
		if messagebus.validate_attributes(attributes):
			self.attributes = attributes

	def update_tx(self):
		self.message_tx.transmit({self.entity_id:self.attributes})

	def observe_other_entity(self,entity_message):	
		entity_id,attributes = entity_message.popitem()
		
		if entity_id == self.entity_id:
			return
		if entity_id in self.other_entities:
			self.other_entities[entity_id].attributes.update(attributes)
		else:
			self.other_entities[entity_id] = Entity({entity_id:attributes})

def run(entity_params_list):
	for i,entity_params in enumerate(entity_params_list): 
		entity = Entity({i:entity_params})
		entity.connect('update',entity.update_tx)
		entity.message_rx.connect('new_message',entity.observe_other_entity)
		event.add_timer(0.1,entity.behaviour.do)
	event.mainloop()

if __name__ == "__main__":

	test_init =   [
			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0,
			'max_age':20,
			'food':5,
			'reproduce_food':50,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0,
			'max_age':20,
			'food':5,
			'reproduce_food':50,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0,
			'max_age':20,
			'food':5,
			'reproduce_food':50,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0,
			'max_age':20,
			'food':5,
			'reproduce_food':50,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			]

	run(test_init)
