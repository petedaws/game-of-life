import random
import math

class Behaviour():

	def __init__(self,entity):
		self.entity = entity	

	def age(self):
		self.entity.attributes['age'] = self.entity.attributes['age'] + self.entity.attributes['age_rate']
		if self.entity.attributes['age'] > self.entity.attributes['max_age']:
			self.entity.die()

	def eat(self,amount):
		self.entity.attributes['food'] = self.entity.attributes['food'] + amount
		if self.entity.attributes['food'] > self.entity.attributes['reproduce_food']:
			self.entity.attributes['food'] = 0.0
			self.entity.emit('spawn')

class RandomMove(Behaviour):

	def do(self):
		self.move()
		self.age()
		self.eat(1)
		self.entity.emit('update')

	def move(self):
		new_x = random.randrange(-1,2)
		new_y = random.randrange(-1,2)
		self.entity.attributes['position_x'] = self.entity.attributes['position_x']+new_x
		self.entity.attributes['position_y'] = self.entity.attributes['position_y']+new_y
		self.entity.emit('update')	

class Stationary(Behaviour):
	def do(self):
		self.entity.emit('update')

class Forage(Behaviour):

	def do(self):
		if self.entity.attributes['state'] != 'dead':
			self.move()
			self.entity.emit('update')

	def move(self):
		if self.entity.attributes['state'] != 'dead':
			closest = self._closest_food()
			if closest is not None and closest[3] > 1.0:
					self.entity.attributes['position_x'] = self.entity.attributes['position_x'] + math.copysign(1,closest[1])
					self.entity.attributes['position_y'] = self.entity.attributes['position_y'] + math.copysign(1,closest[2])

	def _closest_food(self):
		if len(self.entity.other_entities) > 0:
			food_distances = []
			closest = None
			for entity_id in self.entity.other_entities:
				if self.entity.other_entities[entity_id].attributes['type'] == 'grass':
					x_dist = self.entity.other_entities[entity_id].attributes['position_x'] - self.entity.attributes['position_x']
					y_dist = self.entity.other_entities[entity_id].attributes['position_y'] - self.entity.attributes['position_y']
					hypot_dist = math.hypot(x_dist,y_dist)
					food_distances.append((entity_id,x_dist,y_dist,hypot_dist))
					if hypot_dist <= min([dist[3] for dist in food_distances]):
						closest = (entity_id,x_dist,y_dist,hypot_dist)
			return closest


class Combine(Behaviour):

	def __init__(self,entity):
		Behaviour.__init__(self,entity)
		self.avoid = Avoid(self.entity)
		self.ran = RandomMove(self.entity)

class Avoid(Behaviour):
	
	def do(self):
		if self.entity.attributes['state'] != 'dead':
			self.move()
			self.age()
			self.eat(1)
			self.entity.emit('update')

	def move(self):
		if len(self.entity.other_entities) > 0:
			entity_distances = {}
			for entity_id in self.entity.other_entities:	
				if self.entity.other_entities[entity_id].attributes['state'] == 'dead':
					continue				
				x_dist = self.entity.other_entities[entity_id].attributes['position_x'] - self.entity.attributes['position_x']
				y_dist = self.entity.other_entities[entity_id].attributes['position_y'] - self.entity.attributes['position_y']
				hypot_dist = math.hypot(x_dist,y_dist)
				entity_distances[entity_id] = (x_dist,y_dist,hypot_dist)
			move_x = 0
			move_y = 0
			for distance in entity_distances.itervalues():
				if distance[2] == 0:
					move_x = move_x + random.randrange(-4,5)
					move_y = move_y + random.randrange(-4,5)
				if distance[2] < 20:
					move_x = move_x + distance[0]
					move_y = move_y + distance[1]
	
			if move_x != 0.0:
				self.entity.attributes['position_x'] = self.entity.attributes['position_x'] - math.log(abs(move_x))*math.copysign(1,move_x)
			if move_y != 0.0:
				self.entity.attributes['position_y'] = self.entity.attributes['position_y'] - math.log(abs(move_y))*math.copysign(1,move_y)

class Combine(Behaviour):

	def __init__(self,entity):
		Behaviour.__init__(self,entity)
		self.avoid = Avoid(self.entity)
		self.ran = RandomMove(self.entity)

	def move(self):
		if self.entity.attributes['position_x'] > 220 or self.entity.attributes['position_y'] > 220:
			self.ran.do()
		else:
			self.avoid.do()
