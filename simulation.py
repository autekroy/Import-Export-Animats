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
    self.animat_sprite = pygame.image.load("resources/animat.gif")
    self.fruit_sprite = pygame.image.load("resources/dekutree.png")
    self.veggie_sprite = pygame.image.load("resources/Oak-Tree-Sprite.png")

    # picture resources for Alec
    # self.animat_sprite = pygame.image.load("resources/tree.gif")
    # self.animat_sprite.set_colorkey((255,0,255))
    # self.fruit_sprite = pygame.image.load("")
    # self.fruit_sprite.set_colorkey((255,0,255))
    # self.veggie_sprite = pygame.image.load("")
    # self.veggie_sprite.set_colorkey((255,0,255))


    # modify pictures to appropriate sizes
    self.bg = pygame.transform.scale(self.bg, (1000, 700))
    self.fruit_sprite = pygame.transform.scale(self.fruit_sprite, (80, 120))
    self.veggie_sprite = pygame.transform.scale(self.veggie_sprite, (80, 100))

    # initialize the model
    self.env = animats.Environment(num_animats, width, height)


  def update(self):
    self.env.update()


    # for future 'pause' button, the parameter take milliseconds pause time
    # pygame.time.wait()

    # repaint
    self.screen.blit(self.bg, (0,0))

    # set environment: place 2 trees on the top-centered and buttom-centered
    self.screen.blit(self.fruit_sprite, ((self.screenWidth - self.fruit_sprite.get_width())/2, 0)) # on the buttom
    self.screen.blit(self.veggie_sprite, ((self.screenWidth - self.veggie_sprite.get_width())/2, 
                                          self.screenHeight - self.veggie_sprite.get_height()))    # on the top

    # paint animats
    for animat in self.env.animats:
      self.screen.blit(self.animat_sprite, (animat.x, animat.y))
    pygame.display.flip()

if __name__ == "__main__":
  # (width, height, num_animats),  picture maximum size is 800x600
  simulation = Simulation(1000, 700, 40)

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
