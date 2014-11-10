#!/usr/bin/python
import random
import math

class Environment:
  def __init__(self, num_animats, width, height):
    self.width = width
    self.height = height
    self.fruit_tree_pos = ((width - 80) / 2, 0)
    self.veggie_tree_pos = ((width - 80) / 2, height - 80)  
    self.num_animats = num_animats
    self.animats = []
    spawn_x = 100
    spawn_y = 100
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
        new_x = animat.x + (int)(math.cos(animat.direction*math.pi / 180) * 3)
        new_y = animat.y + (int)(math.sin(animat.direction*math.pi / 180) * 3)

	# check wall collision
        if (new_y + 30) > self.height or \
          (new_x + 30) > self.width or \
          new_x < 0 or \
          new_y < 0:
          can_move = False

        # check animat-animat collision	
        others = list(self.animats)
        others.remove(animat)
        for other in others:
	  if pow(new_x - other.x, 2) + pow(new_y - other.y, 2) <= Animat.radius * Animat.radius:
	    can_move = False

        if can_move:
	  animat.x = new_x
	  animat.y = new_y

      # # check death and then reproduce one animat from one of existing animats
      # if animat.fruit_hunger < 0 or animat.veggie_hunger < 0:  
      #   self.animats.remove(animat)
      #   # future code: copy one existing animats' neural network and add mutation

      
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
    decision = int(random.random()*30)

    # forward move in 28/30 possibility
    # can't move until collision is detected
    if decision >= 0 and decision < 28:
      self.wants_to_move = True
    else:
      self.wants_to_move = False

    # rotate left in 1/30 possibility
    if decision == 28:
      self.direction -= 20
    # rotate right in 1/30 possibility
    if decision == 29:
      self.direction += 20

    # get hungry
    energyConsume = 0.5 # energy comsumption unit
    if decision != 4:
      self.fruit_hunger -= energyConsume
      self.veggie_hunger -= energyConsume
