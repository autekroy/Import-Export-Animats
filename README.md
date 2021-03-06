Import-Export-Animats
============================================================
### Course Project for UCLA CS 263C Animats-Based Modeling

### [Project Proposal](https://docs.google.com/document/d/1-vtd3lldCF_84RwrdrOmYrAuGJszBgf5PuqX0CxL8qE)
### [Project Presentation](https://docs.google.com/presentation/d/1nOzJIDy3O5cS1DvDtgHL4e2LRKycsBFy2hNM26x0vPE)
### [Project Report](https://docs.google.com/document/d/1Xxe5j6ea0gBwbp8WcYVyXQ59dWXuPNT9ltiuf0Fl0E8)

#### [Simulation Short Video](http://youtu.be/CIyTv1KNkvs)

#### Dependencies:
* [pybrain](http://www.pybrain.org/)
* [pygame](http://www.pygame.org/)

------------------------------------------------------------
#### How To Run:
* Quick Run: 	               python simulation.py
* Use a save file for animats: python simulation.py filename.dat

#### Quick Model Training Example
* import animats
* e = animats.Environment(10, 1000, 700, "example.dat")
* e.update() # repeat as desired
* e.save()
