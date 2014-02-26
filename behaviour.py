import random
import math

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
			if math.hypot(x_dist,y_dist) < 50:
				if random.choice([True,False]):
					self.entity.attributes['position_x'] = self.entity.attributes['position_x'] - int(math.copysign(1,x_dist))
				else:
					self.entity.attributes['position_y'] = self.entity.attributes['position_y'] - int(math.copysign(1,y_dist))
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
