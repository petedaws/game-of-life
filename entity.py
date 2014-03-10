import subprocess
import messagebus
import time
import event
import sys
import conf
import copy
import random
import scenario
from behaviour import *

class Entity(event.Event):

	def __init__(self,init_attributes):
		event.Event.__init__(self)
		self.other_entities = {}
		self.__init_attributes(init_attributes)
		behav = eval(self.attributes['behaviour'])(self)
		self.behaviour = behav

	def __init_attributes(self,init_attributes):
		self.entity_id,attributes = init_attributes.iteritems().next()
		if messagebus.validate_attributes(attributes):
			self.attributes = attributes

	def get_new_id(self):
		# TODO: need to implement an entity id generator
		return random.randrange(0,50000)

	def update_tx(self):
		message_tx.transmit({self.entity_id:self.attributes})

	def observe_other_entity(self,entity_message):	
		if len(entity_message) < 1:
			return
		for entity_id,attributes in entity_message.iteritems():		
			if entity_id == self.entity_id:
				return
			if entity_id in self.other_entities:
				self.other_entities[entity_id].attributes.update(attributes)
			else:
				self.other_entities[entity_id] = Entity({entity_id:attributes})

	def spawn(self):
		print 'spawn: %d' % self.entity_id
		new_id = self.get_new_id()
		new_attributes = copy.deepcopy(self.attributes)
		new_attributes.update({'age':0.0,'food':5.0})
		entity = Entity({new_id:new_attributes})
		entity.connect('update',entity.update_tx)
		entity.connect('spawn',entity.spawn)
		message_rx.connect('new_message',entity.observe_other_entity)
		event.add_timer(0.1,entity.behaviour.do,'entity%d'%new_id)

	def die(self):
		# TODO: For now this is a memory leak. The object should really die, not just stop the timer.
		print 'die: %d' % self.entity_id
		self.attributes['state'] = 'dead'
		event.modify_timer('entity%d'%self.entity_id,0)
		self.emit('update')

def run(entity_params_list):
	global message_rx
	message_rx = messagebus.MessageRx()
	global message_tx	
	message_tx = messagebus.MessageTx()
	for i,entity_params in enumerate(entity_params_list): 
		entity = Entity({i:entity_params})
		entity.connect('update',entity.update_tx)
		entity.connect('spawn',entity.spawn)
		message_rx.connect('new_message',entity.observe_other_entity)
		event.add_timer(0.1,entity.behaviour.do,'entity%d'%i)
	event.add_io_watcher(message_rx.sock,message_rx.receive)
	event.mainloop()

if __name__ == "__main__":

	if len(sys.argv) < 2:
		run(scenario.scenarios[0])
	else:
		scen = scenario.scenarios[int(sys.argv[1])]
		run(scen)
