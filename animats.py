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
      self.animats.append(Animat(random.random()*width, random.random()*height))

  # TODO - Get this on a thread
  def update(self):
    for animat in self.animats:
      animat.update()
      # check death
      if animat.fruit_hunger < 0 or animat.veggie_hunger < 0:
        self.animats.remove(animat)
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

moves = {
  0: [-2, 0], # left
  1: [2, 0],  # right
  2: [0, -2], # up
  3: [0, 2],  # down
  4: [0, 0]   # no move
}

class Animat:
  def __init__(self, x, y):
    # position
    self.x = x
    self.y = y
    # hunger
    self.fruit_hunger = 10
    self.veggie_hunger = 10 

  def update(self): 
    # movement
    decision = int(random.random()*4)
    self.x += moves[decision][0]
    self.y += moves[decision][1]
    # get hungry
    energyConsume = 0.08 # energy comsumption unit
    if decision != 4:
      self.fruit_hunger -= energyConsume
      self.veggie_hunger -= energyConsume
