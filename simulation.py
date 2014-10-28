#!/usr/bin/python
import animats
import sys # sys.exit()
import pygame

class Simulation:
  def __init__(self, width, height, num_animats):
    # initialize pygame
    pygame.init()

    # initialize the screen
    self.size = width, height
    self.screen = pygame.display.set_mode(self.size)

    #initialize sprites
    self.bg = pygame.image.load("resources/bg.png")
    self.animat_sprite = pygame.image.load("resources/tree.gif")
    self.animat_sprite.set_colorkey((255,0,255))

    # initialize the model
    self.env = animats.Environment(num_animats, width, height)

  def update(self):
    self.env.update()

    # repaint
    self.screen.blit(self.bg, (0,0))
    for animat in self.env.animats:
      self.screen.blit(self.animat_sprite, (animat.x, animat.y))
    pygame.display.flip()

if __name__ == "__main__":
  # maximum size is 800x600
  simulation = Simulation(600,600, 20)
  while 1:
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT: 
        sys.exit()
    simulation.update()
