#!/usr/bin/python

try:
  import wx
except ImportError:
  raise ImportError, "wxPython is required to run this application"

class SimulationApp(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self, parent, id, title)
    self.parent = parent
    self.initialize()

  def initialize(self):
    self.Show(True)

if __name__ == "__main__":
  app = wx.App()
  frame = SimulationApp(None, -1, "Animat Simulation")
  app.MainLoop()