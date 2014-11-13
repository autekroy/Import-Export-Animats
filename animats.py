#!/usr/bin/python
import random
import math
import numpy
from pybrain.tools.shortcuts import buildNetwork

class Environment:
  def __init__(self, num_animats, width, height):
    # environment
    self.width = width
    self.height = height
    
    # trees
    self.fruit_tree = FruitTree(width/2, Tree.radius)
    self.veggie_tree = VeggieTree(width/2, height - Tree.radius)

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

  # get the sum of scents for a type of thing at a certain point
  def scent(self, x, y, thing):
    if thing == Fruit:
      return sum(map(lambda f:f.scent(x,y), self.fruit_tree.foods))
    if thing == Veggie:
      return sum(map(lambda f:f.scent(x,y), self.veggie_tree.foods))

  # TODO - Get this on a thread
  def update(self):
    for animat in self.animats:
      # reset environment sensors
      decision = animat.net.activate([self.scent(animat.x - Animat.radius, \
						 animat.y, Fruit),
				      self.scent(animat.x + Animat.radius, \
						 animat.y, Fruit),
				      self.scent(animat.x - Animat.radius, \
						 animat.y, Veggie),
				      self.scent(animat.x + Animat.radius, \
						 animat.y, Veggie),
				      0,
				      0,
				      animat.fruit_hunger,
				      animat.veggie_hunger,
				      animat.touching])  
      animat.update(decision)
      
      # assume its not touching anything before we check collision
      animat.touching = False 
      if animat.wants_to_move:
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
	# check tree collision
	if pow(new_x - self.fruit_tree.x, 2) \
	 + pow(new_y - self.fruit_tree.y, 2) \
	 <= Tree.radius * Tree.radius \
	or pow(new_x - self.veggie_tree.x, 2) \
	 + pow(new_y - self.veggie_tree.y, 2) \
	 <= Tree.radius * Tree.radius:
	  animat.touching = True
        # check food collision
	for fruit in self.fruit_tree.foods:
	  if pow(new_x - fruit.x, 2) + pow(new_y - fruit.y, 2) \
	   <= Food.radius * Food.radius:
	    animat.touching = True
	    if animat.wants_to_pickup:
	      self.fruit_tree.remove(fruit)
	      animat.food = fruit
	# check veggie collision
	for veggie in self.veggie_tree.foods:
	  if pow(new_x - veggie.x, 2) + pow(new_y - veggie.y, 2) \
	   <= Food.radius * Food.radius:
	    animat.touching = True
	    if animat.wants_to_pickup:
	      self.veggie_tree.remove(veggie)
	      animat.food = veggie
	# check animat-animat collision	
        others = list(self.animats)
        others.remove(animat)
        for other in others:
	  if pow(new_x - other.x, 2) + pow(new_y - other.y, 2) \
	      <= Animat.radius * Animat.radius:
	    animat.touching = True
	# finally move
        if not animat.touching:
	  animat.x = new_x
	  animat.y = new_y
	  animat.get_hungry(1)
     
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
    # 9 sensors: 2 for each smell: fruit, veggie, animat; colliding, 2 hungers
    # 3 hidden layers
    # 6 output nodes: turn left/right, move forward, pickup, putdown, eat
    self.net = buildNetwork(9, 3, 6)  
    

  def update(self, decision): 
    # get a little hungry no matter what
    self.get_hungry(.01 + (decision[1] - decision[2]))

    # move forward, can't move until collision is detected
    self.wants_to_move = (decision[0] > 0)

    # rotate left 
    self.direction -= decision[1]
    # rotate right 
    self.direction += decision[2]

    # pickup
    self.wants_to_pickup = (decision[3] > 0 and not self.food)

    # putdown
    self.wants_to_putdown = ((decision[4] > 0) and self.food)

    # eat
    if (decision[5] > 0) and self.food:
      self.eat()

  def get_hungry(self, amount):
    self.fruit_hunger -= amount
    self.veggie_hunger -= amount
    
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
  def scent(self, x, y):
    return 100.0 / (pow(self.x - x, 2) + pow(self.y - y, 2))
    

class Veggie(Food): pass
class Fruit(Food): pass
