#!/usr/bin/python
import random
import math
import numpy
from pybrain.structure import RecurrentNetwork, FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.supervised.trainers import BackpropTrainer 
from pybrain.datasets import SupervisedDataSet

class Environment:
  def __init__(self, num_animats, width, height):
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
    spawn_x = 100
    spawn_y = 200
    for i in range(0, num_animats):
      if spawn_x > self.width:
        spawn_x = 100
        spawn_y += 100
      self.animats.append(Animat(spawn_x, spawn_y, random.random() * 360))
      spawn_x += 100

  # get the sum of scents for a list of things
  def scent(self, x, y, things):
    return sum(map(lambda f:f.scent(x,y), things))

  # TODO - Get this on a thread
  def update(self):
    # some data
    deaths = []
    all_fruits = [fruit \
		  for fruits in map(lambda f:f.foods, self.fruit_trees) \
		  for fruit in fruits] 
    all_veggies = [veggie \
		   for veggies in map(lambda f:f.foods, self.veggie_trees) \
		   for veggie in veggies]
    for food in self.foods:
      if isinstance(food, Fruit):
	all_fruits.append(food)
      elif isinstance(food, Veggie):
	all_veggies.append(food)
    for animat in self.animats:
      # DEATH
      if animat.fruit_hunger + animat.veggie_hunger < 0:
	deaths.append(animat)
	self.animats.remove(animat)
	continue
      # reset environment sensors
      left_sensor_x = int(math.cos((animat.direction-90)*math.pi/180)*animat.radius)
      left_sensor_y = int(math.sin((animat.direction-90)*math.pi/180)*animat.radius)
      right_sensor_x = int(math.cos((animat.direction+90)*math.pi/180)*animat.radius)
      right_sensor_y = int(math.sin((animat.direction+90)*math.pi/180)*animat.radius)
      has_food = False
      if animat.food:
	has_food = True			    
      animat.update((self.scent(left_sensor_x, left_sensor_y, all_fruits),
		     self.scent(right_sensor_x, right_sensor_y, all_fruits),
		     self.scent(left_sensor_x, left_sensor_y, all_veggies),
		     self.scent(right_sensor_x, right_sensor_y, all_veggies),
		     has_food,
		     animat.fruit_hunger,
		     animat.veggie_hunger,
		     animat.touching))

      if animat.wants_to_move:
	# assume its not touching anything before we check collision
	animat.touching = False 
        # Where does it want to move?
        step = 3
	new_x = animat.x + int(math.cos(animat.direction*math.pi / 180) * step)
        new_y = animat.y + int(math.sin(animat.direction*math.pi / 180) * step)
	# check wall collision
        if (new_y + animat.radius) > self.height \
        or (new_x + animat.radius) > self.width  \
        or (new_x - animat.radius) < 0 \
        or (new_y - animat.radius) < 0:
          animat.touching = True
	# check tree and food on tree collision
	for tree in self.fruit_trees + self.veggie_trees:
	  if pow(new_x - tree.x, 2) + pow(new_y - tree.y, 2) \
	   <= Tree.radius * Tree.radius:
	   animat.touching = True
	  for food in tree.foods:
	    if pow(new_x - food.x, 2) + pow(new_y - food.y, 2) \
	     <= Food.radius * Food.radius:
	      if animat.wants_to_pickup:
		animat.food = food
		tree.foods.remove(food)
	# check food on the ground
	for food in self.foods:
	  if pow(new_x - food.x, 2) + pow(new_y - food.y, 2) \
	   <= Food.radius * Food.radius:
	    if animat.wants_to_pickup:
	      animat.food = food
	      self.foods.remove(food)
	# check animat-animat collision	
        others = list(self.animats)
        others.remove(animat)
        for other in others:
	  if pow(new_x - other.x, 2) + pow(new_y - other.y, 2) \
	      <= Animat.radius * Animat.radius:
	    animat.touching = True
	#check putdown action
	if animat.wants_to_putdown:
	  if isinstance(animat.food, Fruit):
	    self.foods.append(Fruit(animat.x, animat.y))
	  elif isinstance(animat.food, Veggie):
	    self.foods.append(Veggie(animat.x, animat.y))
	  animat.food = None
	# finally move
        if not animat.touching:
	  animat.x = new_x
	  animat.y = new_y
      # reincarnation
      for animat in deaths:
	animat.reincarnate(random.choice(self.animats))
      self.animats += deaths
     
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
    # touching anything
    self.touching = False
    # hunger sensor
    self.fruit_hunger = 1000
    self.veggie_hunger = 1000
    # neural net
    # 8 sensors: 2 for each smell: fruit, veggie; holding; colliding; 2 hungers
    # 3 hidden layers
    # 6 output nodes: turn left/right, move forward, pickup, putdown, eat
    self.net = RecurrentNetwork()
    self.net.addInputModule(LinearLayer(8, name='in'))
    self.net.addModule(SigmoidLayer(3, name='hidden'))
    self.net.addOutputModule(LinearLayer(6, name='out'))
    self.net.addConnection(FullConnection(self.net['in'], self.net['hidden'], name='c1'))
    self.net.addConnection(FullConnection(self.net['hidden'], self.net['out'], name='c2'))
    self.net.addRecurrentConnection(FullConnection(self.net['hidden'], self.net['hidden'], name='c3'))
    self.net.sortModules()
    # Learn by memory:
    # - Keep a short-term memory of actions
    # - When food is found, add those actions to the supervised data set
    self.memories = []
    self.ds = SupervisedDataSet(8, 6)
    self.trainer = BackpropTrainer(self.net, self.ds)
    # thresholds for deciding an action
    self.move_threshold = 0
    self.pickup_threshold = -10
    self.putdown_threshold = -5
    self.eat_threshold = -5
    
  def update(self, sensors):
    decision = self.net.activate(sensors)
    self.memories.append((sensors, decision))
    if len(self.memories) > 10:
      self.memories.remove(self.memories[0])
    #self.ds.addSample(sensors, decision)
    # get a little hungry no matter what
    self.get_hungry(.1)
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
      self.ds.addSample(sensors, decision)
      self.trainer.train()
      self.food = None
      
  def get_hungry(self, amount):
    self.fruit_hunger -= amount
    self.veggie_hunger -= amount

  # reincarnate by cloning neural net and dataset
  def reincarnate(self, other):
    self.fruit_hunger = 1000
    self.veggie_hunger = 1000
    self.net = other.net
    
# Trees
class Tree(object):
  radius = 45
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.foods = []
      
class FruitTree(Tree):
  def __init__(self, x, y):
    super(FruitTree, self).__init__(x,y)
    self.foods.append(Fruit(self.x - self.radius, self.y - 10))
    self.foods.append(Fruit(self.x, self.y + self.radius - 10)) 
    self.foods.append(Fruit(self.x + self.radius, self.y - 10))

class VeggieTree(Tree):
  def __init__(self, x, y):
    super(VeggieTree, self).__init__(x,y)
    self.foods.append(Veggie(self.x - self.radius, self.y))
    self.foods.append(Veggie(self.x, self.y - self.radius))
    self.foods.append(Veggie(self.x + self.radius, self.y))

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
