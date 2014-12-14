
# Trees
class Tree(object):
  radius = 45
  def __init__(self, x, y):
    # flower (position index, age) 
    self.flowers = {} 
    self.x = x
    self.y = y
    self.foods = []

  def pick(self, food):
    self.flowers[self.foods.index(food)] = 0
    self.foods.remove(food)

  def grow(self):
    for i in self.flowers:
      # grow
      self.flowers[i] += 1
      # new food!
      if self.flowers[i] == 50:
	self.spawn(i)
	del(self.flowers[i])
	break
	
# Fruit tree based on Tree class
class FruitTree(Tree):
  def __init__(self, x, y):
    super(FruitTree, self).__init__(x,y)
    self.positions = [(self.x - self.radius, self.y - 10),
		      (self.x, self.y + self.radius - 10),
		      (self.x + self.radius, self.y - 10)]
    self.foods.append(Fruit(self.positions[0][0], self.positions[0][1]))
    self.foods.append(Fruit(self.positions[1][0], self.positions[1][1]))
    self.foods.append(Fruit(self.positions[2][0], self.positions[2][1]))

  def spawn(self, index):
    self.foods.append(Fruit(self.positions[index][0], self.positions[index][1]))

# Veggie tree based on Tree class
class VeggieTree(Tree):
  def __init__(self, x, y):
    super(VeggieTree, self).__init__(x,y)
    self.positions = [(self.x - self.radius, self.y),
		      (self.x, self.y - self.radius),
		      (self.x + self.radius, self.y)]
    self.foods.append(Veggie(self.positions[0][0], self.positions[0][1]))
    self.foods.append(Veggie(self.positions[1][0], self.positions[1][1]))
    self.foods.append(Veggie(self.positions[2][0], self.positions[2][1]))

  def spawn(self, index):
    self.foods.append(Veggie(self.positions[index][0], self.positions[index][1]))
