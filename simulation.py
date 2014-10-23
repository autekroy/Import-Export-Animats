#!/usr/bin/python
import animats
import sys # sys.exit()
import pygame

class Simulation:
  def __init__(self, width, height, num_animats):
    pygame.init()
    self.size = width, height
    self.screen = pygame.display.set_mode(self.size)
    self.env = animats.Environment(num_animats)

  def update(self):
    self.env.update()

if __name__ == "__main__":
  # initialize
  simulation = Simulation(500,500, 10)
  while 1:
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT: 
        sys.exit()

    # update model. TODO - put this on a separate thread
    simulation.update()
    # repaint
    pygame.display.flip()
