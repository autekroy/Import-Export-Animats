Import-Export-Animats
=====================

### Course Project for UCLA CS 263C Animats-Based Modeling

### [Google Docs Project Proposal] (https://docs.google.com/document/d/1-vtd3lldCF_84RwrdrOmYrAuGJszBgf5PuqX0CxL8qE)


#### Hypothesis:
Get Animats to exchange foods at a midpoint between two distant habitats

#### Major Issues:
* Getting the animats to pick up and move food without eating it
* Getting the animats to move the food to the midpoint (learn that is the most effective)
* Getting both sides to cooperate in exchange 

#### Possible Solutions
Animats that randomly decide to carry fruits to the vegetable zone will survive longer.
Imagine they are taking food with them on their journey for themselves after the long walk (for themsevles)
No immediate reward, the reward is in the future when they arrive at their location
They will also have to know to eat it before they drop it
Animat 1 has been eating fruits and is full, and wants vegetables.
By chance, he has the behavior or carrying fruits with him on the journey. This will benefit him in case he gets hungry for fruits along the way.
If he gets to the vegetables and drops his fruit, the other animats on the other side will probably take it, since its the vegetable side and they are probably hungry for fruit
It doesn’t have to learn to share with others yet. This will just get them carrying foods from one side to the other.
After getting benefit from carrying-food behavior, animats will increase their chance to carry food. (higher possibility)
Those carrying-food animats will have more chance to produce next generation due to longer life.
Animats will pass this randomly behavior to their children. (with higher possibility)
Some mutation may happen to next generation. (Super high possibility or super low possibility to carry food.)
With enough animats that know how to take foods on their journeys to the other side, they will start meeting each other in the middle. They have to know to share at this point.

#### Environment:
* 2D
* Non-discrete (not a grid/ free movement)
* No obstacles
* Unlimited Vegetables at bottom, unlimited Fruit at top
* Top and Bottom are cliffs that will kill you
* Left and Right wrap around
* One species, dispersed population

#### Animats:
* Body:
 * Circle
 * Arms are on all sides. When it is colliding with a food, it can do pick up and put down any sides.
* Motors:
 * Move (left, right, up, down. no rotate)
 * Decreases energy faster?
 * Pick up (Food), other animats can’t steal your food from your hands, you have to drop it
 * Put down (Food)
 * Eat (if it has picked up food)
* Sensors:
 * Smell (Strength is inversely proportional to distance):
    * Fruits
    * Vegetables
    * other animats 
 * Hunger for Vegetables (Decreases over time and die when too low, increases when eating)
 * Hunger for Fruits (Decreases over time and die when too low, increase when eating)


#### Experiments for each phases: 
* Phase 1: No obstacles in map. The idea plan is that animats can meet at middle.
* Phase 2: 
  * 1. Center Flower help animals to learn the shortest path.
  * 2. Animals need to drink water. (Add thirsty desire.) To test if animats still will meet each other successfully.
  * Add vision sensor to see pool or river.
  * Add motor to drink.
* Phase 3: Add obstacle like rocks. To see if animats can find shorter or shortest path.
  * Animals may need vision sensor.
  * Animals should have learning skills for remember or recognize shorter path.


#### Details:
* Python 2.7
* pygame
* pyBrain or neurolab

#### How To Run:
* python simulation.py
