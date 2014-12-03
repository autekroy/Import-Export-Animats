#!/usr/bin/python
import random
import math
import numpy
from pybrain.structure import RecurrentNetwork, FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

class Environment:
  # Optionally initialize with a set of neural nets
  def __init__(self, num_animats, width, height, saved_nets=[], train=False):
    # environment
    self.width = width
    self.height = height
    # trees
    self.fruit_trees = [FruitTree(width/2, Tree.radius), \
			FruitTree(Tree.radius + Tree.radius, Tree.radius), \
			FruitTree(width - Tree.radius - Tree.radius, \
				  Tree.radius)]
    self.veggie_trees = [VeggieTree(width/2, height - Tree.radius), \
			 VeggieTree(Tree.radius + Tree.radius, 
				    height - Tree.radius), \
			 VeggieTree(width - Tree.radius - Tree.radius, \
				    height - Tree.radius)]
    # ground foods
    self.foods = []
    # animats
    self.num_animats = num_animats
    self.animats = []
    self.deaths = []
    for i in range(0, num_animats):
      a = Animat(0, 0, random.random() * 360)
      # old neural net
      if saved_nets:
        a.net = saved_nets.pop()
      self.spawn(a)
    
    # Optional training mode: no trees, only random food on the ground
    self.train = train
    if self.train:
      self.fruit_trees = []
      self.veggie_trees = []
      for i in range(0,num_animats/3):
	self.spawn(Fruit(0,0))
	self.spawn(Veggie(0,0))

  # get the sum of scents for a list of things
  def scent(self, x, y, things):
    return sum(map(lambda f:f.scent(x,y), things))

  # places a new animat in a random location on the map
  def spawn(self, thing):
    spawns_x = map(lambda f:f*10, range(0, self.width))
    spawns_y = map(lambda f:f*10, range(0, self.height))
    random.shuffle(spawns_x)
    random.shuffle(spawns_y)
    for i in spawns_x:
      for j in spawns_y:
	if not self.collision(i,j, self.animats):
	  thing.x = i
	  thing.y = j
	  if isinstance(thing, Animat):
	    self.animats.append(thing)
	  else:
	    self.foods.append(thing)
	  return

  def all_fruits(self):
    return [fruit \
	    for fruits in map(lambda f:f.foods, self.fruit_trees + [self]) \
	    for fruit in fruits] 
  def all_veggies(self):
    return [veggie \
	    for veggies in map(lambda f:f.foods, self.veggie_trees + [self]) \
	    for veggie in veggies]

  # TODO - Get this on a thread
  def update(self):
    # tree growth
    for tree in self.fruit_trees + self.veggie_trees:
      tree.grow()
    # foods
    fruits = self.all_fruits()
    veggies = self.all_veggies()
    # food sources
    sources = self.fruit_trees + self.veggie_trees + [self]
    for animat in self.animats:
      # Smell
      #left_sensor_x = int(math.cos((animat.direction-90)*math.pi/180)*animat.radius)+animat.x
      #left_sensor_y = int(math.sin((animat.direction-90)*math.pi/180)*animat.radius)+animat.y
      #right_sensor_x = int(math.cos((animat.direction+90)*math.pi/180)*animat.radius)+animat.x
      #right_sensor_y = int(math.sin((animat.direction+90)*math.pi/180)*animat.radius)+animat.y

      # line of sight
      step_x = int(math.cos(animat.direction*math.pi / 180) * 10)
      step_y = int(math.sin(animat.direction*math.pi / 180) * 10)
      los_x = animat.x
      los_y = animat.y
      sees = None
      while not sees:
	los_x += step_x
	los_y += step_y
	sees = self.collision(los_x, los_y, self.animats)

      has_food = False
      if animat.food:
	has_food = True	
      # inputs are normalized. Possibly not necessary
      animat.update((#self.scent(left_sensor_x, left_sensor_y, fruits),
		     #self.scent(right_sensor_x, right_sensor_y, fruits),
		     #self.scent(left_sensor_x, left_sensor_y, veggies),
		     #self.scent(right_sensor_x, right_sensor_y, veggies),
		     int(isinstance(sees, Fruit))*1000,
		     int(isinstance(sees, Veggie))*1000,
		     int(isinstance(sees, Animat))*1000,
		     int(isinstance(sees, Environment))*1000,
		     int(has_food)*1000,
		     animat.fruit_hunger,
		     animat.veggie_hunger,
		     int(animat.touching)*1000))
      if animat.wants_to_move:
	# Where does it want to move?
        step = 3
	new_x = animat.x + int(math.cos(animat.direction*math.pi / 180) * step)
        new_y = animat.y + int(math.sin(animat.direction*math.pi / 180) * step)
	others = list(self.animats)
	others.remove(animat)
	obstacle = self.collision(new_x, new_y, others)
	# check pickup
	if isinstance(obstacle, Food):
	  for source in sources:
	    if obstacle in source.foods and animat.wants_to_pickup:
	      if isinstance(source, Tree):
		source.pick(obstacle)
	      else:
		source.foods.remove(obstacle)
		if self.train:
		  if isinstance(obstacle, Fruit):
		    source.spawn(Fruit(0,0))
		  else:
		    source.spawn(Veggie(0,0))
	      animat.food = obstacle
      	# finally move if possible
        if not obstacle:
	  animat.x = new_x
	  animat.y = new_y
	else:
	  animat.touching = True
      # putdown
      if animat.wants_to_putdown:
	if isinstance(animat.food, Fruit):
	  self.foods.append(Fruit(animat.x, animat.y))
	elif isinstance(animat.food, Veggie):
	  self.foods.append(Veggie(animat.x, animat.y))
	animat.food = None
      # DEATH 
      if animat not in self.deaths \
      and animat.fruit_hunger + animat.veggie_hunger < 0:
	self.deaths.append(animat)

    # if two animats are pregnant, they mate. Yea it's weird I know
    parents = filter(lambda a: a.pregnant, self.animats)
    if len(parents) >= 2:
      # in case there are more than 2, select 2 random
      parents = random.sample(parents, 2)
      self.spawn(parents[0].mate(parents[1]))
    # keep the population size stable
    while len(self.animats) > self.num_animats and len(self.deaths) > 0:
      self.animats.remove(self.deaths.pop(0))
  
  def collision(self, x, y, animats):
    # check wall collision
    if (y + Animat.radius) > self.height or (x + Animat.radius) > self.width  \
    or (x - Animat.radius) < 0 or (y - Animat.radius) < 0:
      return self
    # check tree collision
    for tree in self.fruit_trees + self.veggie_trees:
      if pow(x - tree.x, 2) + pow(y - tree.y, 2) <= Tree.radius * Tree.radius:
	return tree
    # check food collision
    for food in self.all_fruits() + self.all_veggies():
      if pow(x - food.x, 2) + pow(y - food.y, 2) <= Food.radius * Food.radius:
	return food
    # check animat-animat collision	
    for animat in animats:
      if pow(x - animat.x, 2) + pow(y - animat.y, 2) \
       <= Animat.radius * Animat.radius:
	return animat
    # no collision
    return None

# Animats     
class Animat:
  radius = 30

  def __init__(self, x, y, direction):
    # position
    self.x = x
    self.y = y
    # orientation (0 - 359 degrees)
    self.direction = direction
    # carrying food
    self.food = None
    # ready to mate
    self.pregnant = False
    # touching anything
    self.touching = False
    # hunger sensor
    self.fruit_hunger = 1000
    self.veggie_hunger = 1000
    # neural net
    # 8 sensors: 2 for each smell: fruit, veggie; holding; colliding; 2 hungers
    # 3 hidden layers
    # 6 output nodes: turn left/right, move forward, pickup, putdown, eat
    self.net = FeedForwardNetwork()
    # random layer types
    inputs = [LinearLayer(8, name='in'), SigmoidLayer(8, name='in')]
    hiddens = [LinearLayer(8, name='hidden'), SigmoidLayer(8, name='hidden')]
    outputs = [LinearLayer(6, name='out'), SigmoidLayer(6, name='out')]
    self.net.addInputModule(random.choice(inputs))
    self.net.addModule(random.choice(hiddens))
    self.net.addOutputModule(random.choice(outputs))
    self.net.addConnection(FullConnection(self.net['in'], self.net['hidden']))
    self.net.addConnection(FullConnection(self.net['hidden'], self.net['out']))
    self.net.sortModules()
    # thresholds for deciding an action
    self.move_threshold = 0
    self.pickup_threshold = -1
    self.putdown_threshold = 0
    self.eat_threshold = -5
    
  def update(self, sensors):
    decision = self.net.activate(sensors)
    # get a little hungry no matter what
    self.get_hungry(1)
    # move forward
    self.wants_to_move = (decision[0] > self.move_threshold)
    # rotate left 
    self.direction -= decision[1]
    # rotate right 
    self.direction += decision[2]

    # pickup
    self.wants_to_pickup = ((decision[3] > self.pickup_threshold) 
			    and not self.food)
    # putdown
    self.wants_to_putdown = ((decision[4] > self.putdown_threshold)
			     and self.food)
    # eat
    if (decision[5] > self.eat_threshold) and self.food:
      if isinstance(self.food, Fruit):
	self.fruit_hunger = 1000
      elif isinstance(self.food, Veggie):
	self.veggie_hunger = 1000
      self.food = None
      self.pregnant = True
      
  def get_hungry(self, amount):
    self.fruit_hunger -= amount
    self.veggie_hunger -= amount

  # returns a child with a genetic combination of neural net weights of 2 parents
  def mate(self, other):
    self.pregnant = False
    other.pregnant = False
    child = Animat(0,0, random.random() * 360)
    child.net = FeedForwardNetwork()
    # inherit parents layer types
    child.net.addInputModule(random.choice([self.net['in'], other.net['in']]))
    child.net.addModule(random.choice([self.net['hidden'],other.net['hidden']]))
    child.net.addOutputModule(random.choice([self.net['out'], other.net['out']]))
    # finalize the network
    child.net.addConnection(FullConnection(child.net['in'], child.net['hidden']))
    child.net.addConnection(FullConnection(child.net['hidden'], child.net['out']))
    child.net.sortModules()
    # inherit parents connection weights
    for i in range(0,len(self.net.params)):
      if random.random() > .5:
	child.net.params[i] = self.net.params[i]
      if random.random() < .4:
	child.net.params[i] = other.net.params[i]
      # else, "mutation" - random initial net param not changed
    return child

# Trees
class Tree(object):
  radius = 45
  def __init__(self, x, y):
    # flower (position index, age) 
    self.flowers = {} 
    self.x = x
    self.y = y
    self.foods = []

  def pick(self, food):
    self.flowers[self.foods.index(food)] = 0
    self.foods.remove(food)

  def grow(self):
    for i in self.flowers:
      # grow
      self.flowers[i] += 1
      # new food!
      if self.flowers[i] == 200:
	self.spawn(i)
	del(self.flowers[i])
	break
	
      
class FruitTree(Tree):
  def __init__(self, x, y):
    super(FruitTree, self).__init__(x,y)
    self.positions = [(self.x - self.radius, self.y - 10),
		      (self.x, self.y + self.radius - 10),
		      (self.x + self.radius, self.y - 10)]
    self.foods.append(Fruit(self.positions[0][0], self.positions[0][1]))
    self.foods.append(Fruit(self.positions[1][0], self.positions[1][1]))
    self.foods.append(Fruit(self.positions[2][0], self.positions[2][1]))

  def spawn(self, index):
    self.foods.append(Fruit(self.positions[index][0], self.positions[index][1]))

class VeggieTree(Tree):
  def __init__(self, x, y):
    super(VeggieTree, self).__init__(x,y)
    self.positions = [(self.x - self.radius, self.y),
		      (self.x, self.y - self.radius),
		      (self.x + self.radius, self.y)]
    self.foods.append(Veggie(self.positions[0][0], self.positions[0][1]))
    self.foods.append(Veggie(self.positions[1][0], self.positions[1][1]))
    self.foods.append(Veggie(self.positions[2][0], self.positions[2][1]))

  def spawn(self, index):
    self.foods.append(Veggie(self.positions[index][0], self.positions[index][1]))

# Fruits and Veggies
class Food:
  radius = 20
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.bites = 10
  # scent is inversely proportional to distance
  # 0.0000000001 due to possibility of division by zero
  def scent(self, x, y):
    return 100.0 / (0.000001 + pow(self.x - x, 2) + pow(self.y - y, 2))
    

class Veggie(Food): pass
class Fruit(Food): pass
