#!/usr/bin/python
# Animats environment model
import pickle
import random
import math
import numpy
from pybrain.structure import RecurrentNetwork, FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

# Environment which contains animats and foods
class Environment:
  def __init__(self, num_animats, width, height, filename):
    # training mode (foods everywhere)
    self.training_mode = False
    # environment
    self.width = width
    self.height = height
    # record log
    self.log = []
    self.moveLog = []
    # save state
    self.filename = filename
    # foods
    self.num_foods = num_animats
    self.foods = []
    self.produceFoods
    # animats
    self.num_animats = num_animats
    self.deaths = []
    self.animats = []
    saved_states = self.load()
    while len(self.animats) < num_animats:
      pos = self.findSpace(Animat.radius, (0, self.height))
      if len(saved_states) > 0:
	a = saved_states.pop(0)
	a.x = pos[0]
	a.y = pos[1]
      else:
	a = Animat(pos[0], pos[1], random.random() * 360)
	a.generation = 0
      self.animats.append(a)
    
  # animat line of sight
  def line_of_sight(self, animat):
    step_x = int(math.cos(animat.direction*math.pi / 180) * 10)
    step_y = int(math.sin(animat.direction*math.pi / 180) * 10)
    new_x = animat.x + step_x
    new_y = animat.y + step_y
    sees = None
    while not sees:
      new_x += step_x
      new_y += step_y
      sees = self.collision(new_x, new_y, Animat.radius, animat)
    return sees
  
  # find a random spot to spawn animats
  def findSpace(self, radius, bounds):
    spawns_x = range(0, self.width, 10)
    spawns_y = range(bounds[0], bounds[1], 10)
    random.shuffle(spawns_x)
    random.shuffle(spawns_y)
    for x in spawns_x:
      for y in spawns_y:
	if not self.collision(x, y, radius):
	  return (x, y)
  # return the amount of food in the environment to a fixed state
  def produceFoods(self, train=False):
    fruit_bounds = (0, self.height / 7)
    veggie_bounds =  (self.height - self.height / 7, self.height)
    if self.training_mode:
      fruit_bounds = (0, self.height)
      veggie_bounds = (0, self.height)
    while len(filter(lambda f:isinstance(f,Fruit), self.foods)) < self.num_foods:
      pos = self.findSpace(Food.radius, fruit_bounds)
      self.foods.append(Fruit(pos[0], pos[1]))
    while len(filter(lambda f:isinstance(f,Veggie), self.foods)) < self.num_foods:
      pos = self.findSpace(Food.radius, veggie_bounds)
      self.foods.append(Veggie(pos[0], pos[1]))

  def update(self):
    # if an animat died, the two fittest animats mate
    while len(self.deaths) > 0: 
      fittest = sorted(self.animats, key=lambda a: -a.avg_fruit_hunger -a.avg_veggie_hunger)
      pos = self.findSpace(Animat.radius, (0, self.height))
      child = fittest[0].mate(fittest[1])
      child.x = pos[0]
      child.y = pos[1]
      self.animats.append(child)
      # log experiment data for survival
      tmpLog = (self.deaths[0].generation, self.deaths[0].age )
      self.log.append( tmpLog )
      tmpMoveLog = (self.deaths[0].generation, self.deaths[0].backForth)
      self.moveLog.append( tmpMoveLog )
      self.animats.remove(self.deaths.pop(0))

    for animat in self.animats:
      # update sensory information from environment
      animat.sees = self.line_of_sight(animat)
      step = 3
      step_x = int(math.cos(animat.direction*math.pi / 180) * step)
      step_y = int(math.sin(animat.direction*math.pi / 180) * step)
      animat.touching = self.collision(animat.x + step_x, animat.y + step_y, Animat.radius, animat)
      
      # update animat response to environment
      animat.update()

      # perform animat decided action in environment
      if animat.wants_to_move and \
	(not animat.touching or isinstance(animat.touching,Food)):
	animat.x = step_x + animat.x
	animat.y = step_y + animat.y
      if isinstance(animat.touching, Food) and animat.wants_to_pickup:
	self.foods.remove(animat.touching)
        animat.food = animat.touching
      if animat.wants_to_putdown:
	if isinstance(animat.food, Fruit):
	  self.foods.append(Fruit(animat.x - (step_x*10), animat.y - (step_y*10)))
	elif isinstance(animat.food, Veggie):
	  self.foods.append(Veggie(animat.x - (step_x*10), animat.y - (step_y*10)))
	animat.food = None
      
      # control the amount of food and animats in the environment
      self.produceFoods()
      if animat not in self.deaths \
      and (animat.fruit_hunger + animat.veggie_hunger < 1000):
	self.deaths.append(animat)
        

  def collision(self, x, y, radius, without=None):
    # check wall collision
    if (y + radius) > self.height or (x + radius) > self.width  \
    or (x - radius) < 0 or (y - radius) < 0:
      return self
    # check food collision
    for food in self.foods:
      if (x - food.x)**2 + (y - food.y)**2 <= Food.radius**2:
	return food
    # check animat-animat collision
    animats = list(self.animats)
    if without:
      animats.remove(without)
    for animat in animats:
      if (x - animat.x)**2 + (y - animat.y)**2 <= Animat.radius**2:
	return animat
    # no collision
    return None

  # load saved animat states into environment
  def load(self):
    if self.filename == "":
      return []
    try:
      f = open(self.filename, 'r')
      animats = pickle.load(f)
      f.close()
      return animats
    except:
      print "Could not load file " + self.filename
      return []

  def save(self):
    if self.filename != "":
      f = open(self.filename, 'w')
      pickle.dump(self.animats, f)
      f.close()

# Animats     
class Animat:
  radius = 30

  def __init__(self, x, y, direction):
    self.age = 0
    # position
    self.x = x
    self.y = y
    # number of going back and forth for different foods
    self.backForth = 0
    self.LastFood = None # the last food animat ate
    # orientation (0 - 359 degrees)
    self.direction = direction
    # carrying food
    self.food = None
    # touching anything
    self.touching = None
    self.sees = None
    # hunger sensor
    self.fruit_hunger = 2000
    self.veggie_hunger = 2000
    self.avg_fruit_hunger = 0
    self.avg_veggie_hunger = 0
    # neural net
    self.net = FeedForwardNetwork()
    self.net.addInputModule(LinearLayer(12, name='in'))
    self.net.addModule(SigmoidLayer(13, name='hidden'))
    self.net.addOutputModule(LinearLayer(6, name='out'))
    self.net.addConnection(FullConnection(self.net['in'], self.net['hidden']))
    self.net.addConnection(FullConnection(self.net['hidden'], self.net['out']))
    self.net.sortModules()
    # thresholds for deciding an action
    self.move_threshold = 0
    self.pickup_threshold = 0
    self.putdown_threshold = 0
    self.eat_threshold = 0
    
  def update(self):
    sensors = (2000*int(isinstance(self.sees, Fruit) or \
		        (isinstance(self.sees, Animat) and \
	                 isinstance(self.sees.food, Fruit))),
	       2000*int(isinstance(self.sees, Veggie) or \
	                (isinstance(self.sees, Animat) and \
		         isinstance(self.sees.food, Veggie))),
	       2000*int(isinstance(self.sees, Animat)),
	       2000*int(isinstance(self.sees, Environment)),
	       2000*int(isinstance(self.food, Fruit)),
	       2000*int(isinstance(self.food, Veggie)),
	       self.fruit_hunger,
	       self.veggie_hunger,
	       2000*int(isinstance(self.touching, Fruit) or \
		        (isinstance(self.touching, Animat) and \
		         isinstance(self.touching.food, Fruit))),
	       2000*int(isinstance(self.touching, Veggie) or \
		        (isinstance(self.touching, Animat) and \
		         isinstance(self.touching.food, Veggie))),
	       2000*int(isinstance(self.touching, Animat)),
	       2000*int(isinstance(self.touching, Environment)))
    decision = self.net.activate(sensors)
    
    self.age += 1
    self.get_hungry(.5)
    
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
	self.fruit_hunger = 2000 if (self.fruit_hunger > 1800) else (self.fruit_hunger + 200)
        self.avg_fruit_hunger = (self.avg_fruit_hunger + self.fruit_hunger) / 2
	if isinstance(self.LastFood, Veggie): # the last food is different from eating food
          self.backForth = self.backForth + 1
          print self.backForth
        self.LastFood = Fruit
      elif isinstance(self.food, Veggie):
        self.veggie_hunger = 2000 if (self.veggie_hunger > 1800) else (self.veggie_hunger + 200)
        self.avg_veggie_hunger = (self.avg_veggie_hunger + self.veggie_hunger) / 2
	if isinstance(self.LastFood, Fruit): # the last food is different from eating food
          self.backForth = self.backForth + 1
          print self.backForth
        self.LastFood = Veggie
      self.food = None
      
  def get_hungry(self, amount):
    self.fruit_hunger -= amount
    self.veggie_hunger -= amount

  # returns a child with a genetic combination of neural net weights of 2 parents
  def mate(self, other):
    child = Animat(0,0, random.random() * 360)
    child.generation = min(self.generation, other.generation) + 1
    # inherit parents connection weights
    for i in range(0,len(self.net.params)):
      if random.random() > .1:
	child.net.params[i] = random.choice([self.net.params[i], other.net.params[i]])
    return child

# Fruits and Veggies
class Food:
  radius = 20
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.bites = 10

class Veggie(Food): pass
class Fruit(Food): pass
