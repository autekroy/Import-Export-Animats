#!/usr/bin/python
import animats
import sys  # sys.exit()
import pygame
import math

class Simulation:
  def __init__(self, num_animats, width, height, saved_nets):
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
    
    # pictures resources
    self.animat_sprite  = pygame.image.load("resources/animat.png")
    self.fruit          = pygame.image.load("resources/banana.png")
    self.veggie         = pygame.image.load("resources/tomato.png")

    # modify pictures to appropriate sizes
    self.animat_sprite = pygame.transform.scale(self.animat_sprite, (32,32))
    self.bg            = pygame.transform.scale(self.bg, (1000, 700))
    self.fruit         = pygame.transform.scale(self.fruit, (26, 26))
    self.veggie        = pygame.transform.scale(self.veggie, (26, 26))

    self.env = animats.Environment(num_animats, width, height, saved_nets)

  def update(self, speed):
    # update model a certain number of times
    for i in range(speed):
      self.env.update()

    # for future 'pause' button, the parameter take milliseconds pause time
    # pygame.time.wait()

    # repaint
    self.screen.blit(self.bg, (0,0))

    # paint food
    for food in self.env.foods:
	if isinstance(food, animats.Fruit):
	  self.screen.blit(self.fruit, \
			   (food.x - animats.Food.radius, \
			    food.y - animats.Food.radius))
	else:
	  self.screen.blit(self.veggie, \
			   (food.x - animats.Food.radius, \
			    food.y - animats.Food.radius))

    # paint animats
    for animat in self.env.animats:
      self.screen.blit(pygame.transform.rotate(self.animat_sprite, 360 - animat.direction), (animat.x - animats.Animat.radius, animat.y - animats.Animat.radius))
      if animat.food:
	if isinstance(animat.food, animats.Fruit):
	  self.screen.blit(self.fruit, \
			   (animat.x - animats.Animat.radius, \
			    animat.y - animats.Animat.radius))
	elif isinstance(animat.food, animats.Veggie):
	  self.screen.blit(self.veggie, \
			   (animat.x - animats.Animat.radius, \
			    animat.y - animats.Animat.radius))

    pygame.display.flip()

if __name__ == "__main__":
  # load save state from file
  filename = ""
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  simulation = Simulation(10, 1000, 700, filename)
  
  # main loop
  while 1: 
    for event in pygame.event.get():
      # check for exit
      if event.type == pygame.QUIT: 
	simulation.env.save()
	# save record log
	fLog = open("log.txt",'w')
	map(lambda r: fLog.write( str(r) + '\n'), simulation.env.log)
	fLog.close()
        sys.exit()
    simulation.update(10)
