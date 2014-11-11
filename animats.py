#!/usr/bin/python
import random
import math

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
        move_step = 3;
        new_x = animat.x + (int)(math.cos(animat.direction*math.pi / 180) * move_step)
        new_y = animat.y + (int)(math.sin(animat.direction*math.pi / 180) * move_step)

	# check wall collision
        if (new_y + Animat.radius) > self.height \
        or (new_x + Animat.radius) > self.width  \
        or (new_x - Animat.radius) < 0 \
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

        # check animat-animat collision	
        others = list(self.animats)
        others.remove(animat)
        for other in others:
	  if pow(new_x - other.x, 2) + pow(new_y - other.y, 2) \
	      <= Animat.radius * Animat.radius:
	    can_move = False

        if can_move:
	  animat.x = new_x
	  animat.y = new_y

      # # check death and then reproduce one animat from one of existing animats
      # if animat.fruit_hunger < 0 or animat.veggie_hunger < 0:  
      #   self.animats.remove(animat)
      #   # future code: copy one existing animats' neural network and add mutation
     
# Animats     
class Animat:
  radius = 30

  def __init__(self, x, y, direction):
    # position
    self.x = x
    self.y = y
    # orientation (0 - 359 degrees)
    self.direction = direction
    # hunger
    self.fruit_hunger = 20 + random.random() * 10;
    self.veggie_hunger = 20 + random.random() * 10;

  def update(self): 
    # random action
    decision = int(random.random()*20)

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

# Trees
class Tree(object):
  radius = 60
  def __init__(self, x, y):
    print "initing_tree"
    self.x = x
    self.y = y
      
class FruitTree(Tree):
  def __init__(self, x, y):
    super(FruitTree, self).__init__(x,y)
    self.foods = (Fruit(self.x - self.radius, self.y), \
		  Fruit(self.x, self.y + self.radius), \
		  Fruit(self.x + self.radius, self.y))

class VeggieTree(Tree):
  def __init__(self, x, y):
    super(VeggieTree, self).__init__(x,y)
    self.foods = (Veggie(self.x - self.radius, self.y), \
		  Veggie(self.x, self.y - self.radius), \
		  Veggie(self.x + self.radius, self.y))

# Fruits and Veggies
class Food:
  radius = 20
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.bites = 10
    

class Veggie(Food): pass
class Fruit(Food): pass
