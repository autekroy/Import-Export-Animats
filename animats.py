#!/usr/bin/python
import random

class Environment:
  def __init__(self, num_animats):
    self.num_animats = num_animats
    self.animats = []
    for i in range(0, num_animats):
      self.animats.append(Animat(0, 0, random.random(), random.random()))

  # TODO - Get this on a thread to continuously update
  def update(self):
    for animat in self.animats:
      animat.update()

class Animat:
  def __init__(self, x, y, vx, vy):
    self.x = x
    self.y = y
    self.vx = -1
    self.vy = 0

  def update(self): 
    self.x += self.vx
    self.y += self.vy

