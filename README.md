Import-Export-Animats
=====================

### Course Project for UCLA CS 263C Animats-Based Modeling

### [Google Docs Project Proposal] (https://docs.google.com/document/d/1-vtd3lldCF_84RwrdrOmYrAuGJszBgf5PuqX0CxL8qE)


#### Hypothesis:
A species of animats that live in a world where the sources of two foods essential to their survival exist entirely in two distant locations will evolve and learn to transport and exchange those foods at the midpoint between those locations.

#### Major Issues:
* Getting the animats to pick up and move food without eating it.
* Getting the animats to share food
* Getting the animats to cooperate in altruistic behavior
* Getting the animats to learn to exchange at the midpoint between the habitats

#### Methodology: 
* Focuses on group level cooperation and exchange.
* Eliminates certain details at the individual level, such as foraging techniques, motor control and reproduction. 
* The goal is to challenge the costly lifestyle of inefficient traveling to hunt for food.

#### Physics:
* 2D Map: Collision among all objects. Nothing can climb over something or go under it
* Continuous: Movement is entirely free and not grid-like
* Top and Bottom are walls
* Left and Right borders wrap around to each other

#### Environment:
* There are a few trees on the top to spawn unlimited vegetables, and a few trees on the bottom to spawn unlimited fruit
* One species of animats of a variable size at startup, initially distributed evenly across map. 
 * This is going to be a tuning parameter, to see how it affects our outcome. 
 * If one animat dies, one random animat of the remaining survivors will asexually reproduce, keeping the population size constant.

![Fruit](/resources/banana.png)  ![tomato](/resources/tomato.png)

#### Animats:
* Brain:
 * Adaptive neural network connecting sensors and motors
 * The neural network structure will be fixed and the weights will change over time.
 * “Reproduction” will spawn a new animat with a copy of the neural network with some mutation.
* Body:
 * Circular: No appendages. The face of the animat is shown on the body.
 * Mouth: when the circular body is colliding with a fruit or vegetable on its face side, it can pick it up with its mouth. 
* Motors:
 * Move forward: Fixed speed, takes energy
 * Rotate (Left, Right): Fixed speed, takes no energy
 * Pick up (Food): 
    * If it is touching food, then it can pick it up. 
    * Only 1 at a time, face will be small enough such that its face can’t be colliding with more than 1 at a time. 
    * Other animats can’t steal your food from your mouth
 * Put down (if it has picked up food)
 * Eat (if it has picked up food): 
    * Divided into a certain number of bites.
    * Increases energy
* Sensors:
 * Touch: If its face is within a certain distance of food (i.e. colliding with it)
 * Smell (Strength is inversely proportional to distance):
    * Fruits
    * Vegetables
    * Other animats 
 * Hunger (energy level): decreases over time at a constant rate (faster when moving) and the animat will die if one of two energy level is too low. 
    * Vegetables
    * Fruits


#### Overall System Model:
* Mostly neural network with adapting weights, supported by evolution to naturally select smarter networks to pass on to next generations.

#### Phases:
* Phase 1: Initial hypothesis, cooperative exchange.
* Phase 2: Introduce 2 new types of food and locations, and observe the exchange patterns.

#### Language/Tools:
* Python 2.7
* pyBrain or neurolab for neural network
* pygame for graphics

#### How To Run:
* python simulation.py

#### Install
* pybrain:
 * $ git clone git://github.com/pybrain/pybrain.git
 * $ python setup.py install
 * Tutorials: http://pybrain.org/docs/index.html?highlight=neural%20network
