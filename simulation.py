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
    self.screenWidth = width
    self.screenHeight = height

    # set the name of display windows
    pygame.display.set_caption('Import/Export project')

    #initialize sprites
    self.bg = pygame.image.load("resources/bg.png")
    
    # pictures resources for Yao-Jen
    self.animat_sprite  = pygame.image.load("resources/animat.png")
    self.fruitTree      = pygame.image.load("resources/dekutree.png")
    self.veggieTree     = pygame.image.load("resources/dekutree.png")
    self.fruit          = pygame.image.load("resources/banana.png")
    self.veggie         = pygame.image.load("resources/tomato.png")

    # modify pictures to appropriate sizes
    self.animat_sprite = pygame.transform.scale(self.animat_sprite, (32,32))
    self.bg            = pygame.transform.scale(self.bg, (1000, 700))
    self.fruitTree     = pygame.transform.scale(self.fruitTree, (80, 100))
    self.veggieTree    = pygame.transform.scale(self.veggieTree, (80, 100))
    self.fruit         = pygame.transform.scale(self.fruit, (26, 26))
    self.veggie        = pygame.transform.scale(self.veggie, (26, 26))

    # initialize the model
    self.env = animats.Environment(num_animats, width, height)

  def update(self):
    self.env.update()

    # for future 'pause' button, the parameter take milliseconds pause time
    # pygame.time.wait()

    # repaint
    self.screen.blit(self.bg, (0,0))

    # paint trees
    self.screen.blit(self.fruitTree, \
                    (self.env.fruit_tree.x - animats.Tree.radius, \
		    self.env.fruit_tree.y - animats.Tree.radius))
    self.screen.blit(self.veggieTree, \
                    (self.env.veggie_tree.x - animats.Tree.radius, \
		    self.env.veggie_tree.y - animats.Tree.radius))

    # paint animats
    for animat in self.env.animats:
      self.screen.blit(pygame.transform.rotate(self.animat_sprite, 360 - animat.direction), (animat.x - animats.Animat.radius, animat.y - animats.Animat.radius))
      # self.screen.blit(self.fruit, (animat.x - self.fruit.get_width()/2, animat.y - self.fruit.get_height()))
      # self.screen.blit(self.veggie, (animat.x + self.veggie.get_width()/2, animat.y - self.veggie.get_height()))

    pygame.display.flip()

if __name__ == "__main__":
  # (width, height, num_animats),  picture maximum size is 800x600
  simulation = Simulation(1000, 700, 15)

  # try to add slider and button
  # master = Tk()
  # Button(master, text='Show', command=show_values).pack()
  # # w = Scale(master, from_=0, to=42)
  # # w.pack()
  # w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
  # w.pack()

  while 1: # main loop
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT: 
        sys.exit()
    simulation.update()
