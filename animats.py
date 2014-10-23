#!/usr/bin/python
import random

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
    self.x = x
    self.y = y
    self.vx = random.random()
    self.vy = random.random()

  def set_vx(self, vx):
    self.vx = vx
  def set_vy(self, vy):
    self.vy = vy

  def update(self): 
    self.x += self.vx
    self.y += self.vy

