import subprocess
import messagebus
import time
import event
import sys
import conf
import copy
import random
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
		self.connect('spawn',self.spawn)
		event.add_io_watcher(self.message_rx.sock,self.message_rx.receive)


	def __init_attributes(self,init_attributes):
		self.entity_id,attributes = init_attributes.iteritems().next()
		if messagebus.validate_attributes(attributes):
			self.attributes = attributes

	def get_new_id(self):
		# TODO: need to implement an entity id generator
		return random.randrange(0,50000)

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

	def spawn(self):
		new_id = self.get_new_id()
		new_attributes = copy.deepcopy(self.attributes)
		new_attributes.update({'age':0.0,'food':5.0})
		entity = Entity({new_id:new_attributes})
		entity.connect('update',entity.update_tx)
		entity.message_rx.connect('new_message',entity.observe_other_entity)
		event.add_timer(0.1,entity.behaviour.do,'entity%d'%new_id)

	def die(self):
		# TODO: For now this is a memory leak. The object should really die, not just stop the timer.
		self.attributes['state'] = 'dead'
		event.modify_timer('entity%d'%self.entity_id,0)
		self.emit('update')

def run(entity_params_list):
	for i,entity_params in enumerate(entity_params_list): 
		entity = Entity({i:entity_params})
		entity.connect('update',entity.update_tx)
		entity.message_rx.connect('new_message',entity.observe_other_entity)
		event.add_timer(0.1,entity.behaviour.do,'entity%d'%i)
	event.mainloop()

if __name__ == "__main__":

	test_init1 =   [
			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0.0,
			'max_age':2000.0,
			'age_rate':0.2,
			'food':5.0,
			'reproduce_food':500.0,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},
			]

	test_init =   [
			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0.0,
			'max_age':20.0,
			'age_rate':0.1,
			'food':5.0,
			'reproduce_food':50.0,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0.0,
			'max_age':20.0,
			'age_rate':0.1,
			'food':5.0,
			'reproduce_food':50.0,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0.0,
			'max_age':20.0,
			'age_rate':0.1,
			'food':5.0,
			'reproduce_food':50.0,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			{
			'position_x':320,
			'position_y':250,
			'type':'grass',
			'state':'alive',
			'age':0.0,
			'max_age':20.0,
			'age_rate':0.1,
			'food':5.0,
			'reproduce_food':50.0,
			'max_speed':5.0,
			'behaviour':'Avoid',
			},

			]

	run(test_init)
