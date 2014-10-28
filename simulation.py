#!/usr/bin/python
import animats
import sys # sys.exit()
import pygame
import wx

class Simulation:
  def __init__(self, width, height, num_animats):
    # initialize pygame
    pygame.init()

    # initialize the screen
    self.size = width, height
    self.screen = pygame.display.set_mode(self.size)

    # set the name of display windows
    pygame.display.set_caption('Import/Export project')

    #initialize sprites
    self.bg = pygame.image.load("resources/bg.gif")
    self.animat_sprite = pygame.image.load("resources/dekutree.png")
    # self.animat_sprite.set_colorkey((255,0,255))

    # initialize the model
    self.env = animats.Environment(num_animats, width, height)


  def update(self):
    self.env.update()

    # for future 'pause' button, the parameter take milliseconds pause time
    # pygame.time.wait()

    # repaint
    self.screen.blit(self.bg, (0,0))
    for animat in self.env.animats:
      self.screen.blit(self.animat_sprite, (animat.x, animat.y))
    pygame.display.flip()

if __name__ == "__main__":
  # maximum size is 800x600
  simulation = Simulation(600,600, 100)


  while 1: # main loop
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT: 
        sys.exit()
    simulation.update()
