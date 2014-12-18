#!/usr/bin/python
import pickle
import random
import math
import numpy
from pybrain.structure import RecurrentNetwork, FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

class Environment:
  def __init__(self, num_animats, width, height, filename):
    # environment
    self.width = width
    self.height = height
    # record log
    self.log = []
    # save state
    self.filename = filename
    # foods
    self.num_foods = num_animats
    self.foods = []
    self.produceFoods
    # animats
    self.num_animats = num_animats
    self.animats = []
    self.deaths = []
    saved_nets = self.load()
    for i in range(0, num_animats):
      pos = self.findSpace(Animat.radius, (0, self.height))
      a = Animat(pos[0], pos[1], random.random() * 360)
      a.generation = 1
      # old neural net
      if saved_nets:
        a.net = saved_nets.pop()
      self.animats.append(a)
    
  # get the sum of scents for a list of things
  def scent(self, x, y, things):
    return sum(map(lambda f:f.scent(x,y), things))

  # line of sight
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

  def findSpace(self, radius, bounds):
    spawns_x = range(0, self.width, 10)
    spawns_y = range(bounds[0], bounds[1], 10)
    random.shuffle(spawns_x)
    random.shuffle(spawns_y)
    for x in spawns_x:
      for y in spawns_y:
	if not self.collision(x, y, radius):
	  return (x, y)

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
      fittest = sorted(self.animats, key=lambda a: \
				     -a.age -a.fruit_hunger - a.veggie_hunger)
      pos = self.findSpace(Animat.radius, (0, self.height))
      child = fittest[0].mate(fittest[1])
      child.x = pos[0]
      child.y = pos[1]
      self.animats.append(child)
      for a in fittest:
        if a.generation == fittest[0].generation:
          tmp = (fittest[0].generation, a.fruit_hunger + a.veggie_hunger ) 
          self.log.append( tmp )
      self.animats.remove(self.deaths.pop(0))
    # update each animat
    for animat in self.animats:
      # Smell
      #left_sensor_x = int(math.cos((animat.direction-90)*math.pi/180)*animat.radius)+animat.x
      #left_sensor_y = int(math.sin((animat.direction-90)*math.pi/180)*animat.radius)+animat.y
      #right_sensor_x = int(math.cos((animat.direction+90)*math.pi/180)*animat.radius)+animat.x
      #right_sensor_y = int(math.sin((animat.direction+90)*math.pi/180)*animat.radius)+animat.y
      # Sight
      sees = self.line_of_sight(animat)
      # Touch
      step = 3
      new_x = animat.x + int(math.cos(animat.direction*math.pi / 180) * step)
      new_y = animat.y + int(math.sin(animat.direction*math.pi / 180) * step)
      touching = self.collision(new_x, new_y, Animat.radius, animat)
      # update
      animat.update((#self.scent(left_sensor_x, left_sensor_y, fruits),
		     #self.scent(right_sensor_x, right_sensor_y, fruits),
		     #self.scent(left_sensor_x, left_sensor_y, veggies),
		     #self.scent(right_sensor_x, right_sensor_y, veggies),
		     int(isinstance(sees, Fruit))*1000,
		     int(isinstance(sees, Veggie))*1000,
		     int(isinstance(sees, Animat))*1000,
		     int(isinstance(sees, Environment))*1000,
		     int(isinstance(animat.food, Fruit))*1000,
		     int(isinstance(animat.food, Veggie))*1000,
		     animat.fruit_hunger,
		     animat.veggie_hunger,
		     int(isinstance(touching, Fruit))*1000,
		     int(isinstance(touching, Veggie))*1000,
		     int(isinstance(touching, Animat))*1000,
		     int(isinstance(touching, Environment))*1000))
      # moving
      if animat.wants_to_move and (not touching or isinstance(touching,Food)):
	animat.x = new_x
	animat.y = new_y

      # pickup
      if isinstance(touching, Food) and animat.wants_to_pickup:
	self.foods.remove(touching)
        animat.food = touching
      # putdown
      if animat.wants_to_putdown:
	if isinstance(animat.food, Fruit):
	  self.foods.append(Fruit(animat.x, animat.y))
	elif isinstance(animat.food, Veggie):
	  self.foods.append(Veggie(animat.x, animat.y))
	animat.food = None
      # keep the food supply constant
      self.produceFoods()
      # DEATH 
      if animat not in self.deaths \
      and (animat.fruit_hunger + animat.veggie_hunger <= 0):
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

  # load neural net states
  def load(self):
    if self.filename == "":
      return []
    try:
      f = open(self.filename, 'r')
      nets = pickle.load(f)
      f.close()
      return nets
    except:
      print "Could not load file " + self.filename
      return []

  # save neural net states
  def save(self):
    if self.filename != "":
      f = open(self.filename, 'w')
      nets = map(lambda a:a.net, self.animats)
      pickle.dump(nets, f)
      f.close()

# Animats     
class Animat:
  radius = 30

  def __init__(self, x, y, direction):
    # position
    self.age = 0
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
    self.net = FeedForwardNetwork()
    self.net.addInputModule(SigmoidLayer(12, name='in'))
    self.net.addModule(SigmoidLayer(20, name='hidden'))
    self.net.addOutputModule(LinearLayer(6, name='out'))
    self.net.addConnection(FullConnection(self.net['in'], self.net['hidden']))
    self.net.addConnection(FullConnection(self.net['hidden'], self.net['out']))
    self.net.sortModules()
    # thresholds for deciding an action
    self.move_threshold = 0
    self.pickup_threshold = -1
    self.putdown_threshold = 0
    self.eat_threshold = -4
    
  def update(self, sensors):
    decision = self.net.activate(sensors)
    # get a little hungry no matter what
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
        self.fruit_hunger = 1000 if (self.fruit_hunger > 950) else (self.fruit_hunger + 50)
      elif isinstance(self.food, Veggie):
        self.veggie_hunger = 1000 if (self.veggie_hunger > 950) else (self.veggie_hunger + 50)
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
  # normalization to prevent divide by 0
  def scent(self, x, y):
    return 100.0 / (0.000001 + pow(self.x - x, 2) + pow(self.y - y, 2))
    

class Veggie(Food): pass
class Fruit(Food): pass
