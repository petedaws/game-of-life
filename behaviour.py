import random

class Behaviour():

	def __init__(self,entity):
		self.entity = entity	

class RandomMove(Behaviour):

	def do(self):
		new_x = random.randrange(-1,2)
		new_y = random.randrange(-1,2)
		self.entity.attributes['position_x'] = self.entity.attributes['position_x']+new_x
		self.entity.attributes['position_y'] = self.entity.attributes['position_y']+new_y
		self.entity.emit('update')	

class Avoid(Behaviour):
	
	def do(self):
		for entity_id in self.entity.other_entities:
			x_dist = self.entity.other_entities[entity_id].attributes['position_x'] - self.entity.attributes['position_x']
			y_dist = self.entity.other_entities[entity_id].attributes['position_y'] - self.entity.attributes['position_y']
			if abs(x_dist) < 50:
				self.entity.attributes['position_x'] = self.entity.attributes['position_x'] + 1
			if abs(y_dist) < 50:
				self.entity.attributes['position_y'] = self.entity.attributes['position_y'] + 1
		self.entity.emit('update')

class Combine(Behaviour):

	def __init__(self,entity):
		Behaviour.__init__(self,entity)
		self.avoid = Avoid(self.entity)
		self.ran = RandomMove(self.entity)

	def do(self):
		if self.entity.attributes['position_x'] > 220 or self.entity.attributes['position_y'] > 220:
			self.ran.do()
		else:
			self.avoid.do()
