#!/usr/bin/python
import animats
import sys # sys.exit()
import pygame
<<<<<<< HEAD
import wx
=======
>>>>>>> 5ec611f1d19939deffd0ae5474521a6096ba816f

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
<<<<<<< HEAD
    self.bg = pygame.image.load("resources/bg.gif")
    self.animat_sprite = pygame.image.load("resources/dekutree.png")
    # self.animat_sprite.set_colorkey((255,0,255))
=======
    self.bg = pygame.image.load("resources/bg.png")
    self.animat_sprite = pygame.image.load("resources/tree.gif")
    self.animat_sprite.set_colorkey((255,0,255))
>>>>>>> 5ec611f1d19939deffd0ae5474521a6096ba816f

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
<<<<<<< HEAD
  simulation = Simulation(600,600, 100)

=======
  simulation = Simulation(600,600, 20)
  # try to add slider and button
  # master = Tk()
  # Button(master, text='Show', command=show_values).pack()
  # # w = Scale(master, from_=0, to=42)
  # # w.pack()
  # w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
  # w.pack()
>>>>>>> 5ec611f1d19939deffd0ae5474521a6096ba816f

  while 1: # main loop
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT: 
        sys.exit()
    simulation.update()
