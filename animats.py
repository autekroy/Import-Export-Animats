#!/usr/bin/python
import random
import math

class Environment:
  def __init__(self, num_animats, width, height):
    self.width = width
    self.height = height
    self.num_animats = num_animats
    self.animats = []
    for i in range(0, num_animats):
      self.animats.append(Animat(random.random() * width,
                                 random.random() * height, 
                                 random.random() * 360))

  # TODO - Get this on a thread
  def update(self):
    for animat in self.animats:
      animat.update()
      
      # # check death and then reproduce one animat from one of existing animats
      # if animat.fruit_hunger < 0 or animat.veggie_hunger < 0:  
      #   self.animats.remove(animat)
      #   # future code: copy one existing animats' neural network and add mutation

      # check ceiling/floor collision
      if animat.y < 0:
        animat.y = 0
      if (animat.y + 30) > self.height:
        animat.y = self.height - 30
      # wrap-around left and right border
      if (animat.x + 30) < 0:
        animat.x = self.width
      if animat.x > self.width:
        animat.x = 0

class Animat:
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
    decision = int(random.random()*3)

    # forward move
    if decision == 0:
      self.x += math.cos(self.direction*math.pi / 180)
      self.y += math.sin(self.direction*math.pi / 180)
    # # rotate left
    # if decision == 1:
    #   self.direction -= 20
    # # rotate right
    # if decision == 2:
    #   self.direction += 20


    # get hungry
    energyConsume = 0.5 # energy comsumption unit
    if decision != 4:
      self.fruit_hunger -= energyConsume
      self.veggie_hunger -= energyConsume
