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
      self.animats.append(Animat(0, 0, random.random(), random.random()))

  # TODO - Get this on a thread
  def update(self):
    for animat in self.animats:
      animat.update()
      # check death
      if animat.fruit_hunger < 0 or animat.veggie_hunger < 0:
        self.animats.remove(animat)

      # check ceiling/floor collision
      if animat.y < 0 or (animat.y + 30) > self.height:
        animat.vy = animat.vy * -1
      # wrap-around left and right border
      if (animat.x + 30) < 0:
        animat.x = self.width
      if animat.x > self.width:
        animat.x = 0


class Animat:
  def __init__(self, x, y, vx, vy):
    # kinetics
    self.x = x
    self.y = y
    self.vx = (random.random() - .5) # range [-.5, .5]
    self.vy = (random.random() - .5) # range [-.5, .5]

    # hunger
    self.fruit_hunger = 10
    self.veggie_hunger = 10

  def set_vx(self, vx):
    self.vx = vx
  def set_vy(self, vy):
    self.vy = vy

  def update(self): 
    self.x += self.vx
    self.y += self.vy
    # get hungry
    self.fruit_hunger -= .01*math.sqrt(self.vx*self.vx + self.vy*self.vy)
    self.veggie_hunger -= .01*math.sqrt(self.vx*self.vx + self.vy*self.vy)
