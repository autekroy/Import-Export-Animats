#!/usr/bin/python
import random
import math
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

  # TODO - Get this on a thread
  def update(self):
    for animat in self.animats:
      animat.update()
      
      can_move = True
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
          can_move = False
	# check tree collision
	if pow(new_x - self.fruit_tree.x, 2) \
	 + pow(new_y - self.fruit_tree.y, 2) \
	 <= Tree.radius * Tree.radius \
	or pow(new_x - self.veggie_tree.x, 2) \
	 + pow(new_y - self.veggie_tree.y, 2) \
	 <= Tree.radius * Tree.radius:
	    can_move = False
        # check food collision
	for fruit in self.fruit_tree.foods:
	  if pow(new_x - fruit.x, 2) + pow(new_y - fruit.y, 2) \
	   <= Food.radius * Food.radius:
	    # temporary auto-pickup
	    if(animat.trypickup(fruit)):
	      self.fruit_tree.foods.remove(fruit)
	    can_move = False
	# check veggie collision
	for veggie in self.veggie_tree.foods:
	  if pow(new_x - veggie.x, 2) + pow(new_y - veggie.y, 2) \
	   <= Food.radius * Food.radius:
	    # temporary auto-pickup
	    if(animat.trypickup(veggie)):
	      self.veggie_tree.foods.remove(veggie)
	    can_move = False
	# check animat-animat collision	
        others = list(self.animats)
        others.remove(animat)
        for other in others:
	  if pow(new_x - other.x, 2) + pow(new_y - other.y, 2) \
	      <= Animat.radius * Animat.radius:
	    can_move = False
	# finally move
        if can_move:
	  animat.x = new_x
	  animat.y = new_y

     
# Animats     
class Animat:
  radius = 30

  def __init__(self, x, y, direction):
    # position
    self.x = x
    self.y = y
    # orientation (0 - 359 degrees)
    self.direction = direction

    # smell sensor
    self.left_smell_fruit = random.random() * 5;
    self.right_smell_fruit = random.random() * 5;
    self.left_smell_veggie = random.random() * 5;
    self.right_smell_veggie = random.random() * 5;

    self.left_smell_animat = random.random() * 5;
    self.right_smell_animat = random.random() * 5;
  
    # carrying food
    self.food = None

    # hunger sensor
    self.fruit_hunger = 20 + random.random() * 10;
    self.veggie_hunger = 20 + random.random() * 10;

    # touch sensor
    self.touch_food = random.random() * 5;

    # built simple neural network
    # 9 input layers, 3 hidden layers, and 1 output layer
    self.net = buildNetwork(9, 3, 1)  
    

  def update(self): 
    # random action
    # decision = int(random.random()*20)

    # neural network action
    # don't know about the output range.. check it later
    decision = self.net.activate([self.left_smell_fruit, self.right_smell_fruit, \
          self.left_smell_veggie, self.right_smell_veggie, \
          self.left_smell_animat, self.right_smell_animat, \
          self.fruit_hunger, self.veggie_hunger, self.touch_food
      ])[0] * 100 % 20;

    # forward move in 28/30 possibility
    # can't move until collision is detected
    if decision >= 0 and decision < 19:
      self.wants_to_move = True
    else:
      self.wants_to_move = False

    # rotate left in 1/30 possibility
    if decision == 19:
      self.direction -= 20
    # rotate right in 1/30 possibility
    if decision == 20:
      self.direction += 20

    # get hungry
    energyConsume = 0.5 # energy comsumption unit
    if decision != 4:
      self.fruit_hunger -= energyConsume
      self.veggie_hunger -= energyConsume

  def trypickup(self, food):
    if not self.food:
      self.food = food
      return True
    else:
      return False

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
    

class Veggie(Food): pass
class Fruit(Food): pass
