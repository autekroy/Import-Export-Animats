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
    # Grid layout
    self.sizer = wx.BoxSizer(wx.VERTICAL)

    # Background image
    self.bg = wx.Image('bg.gif', wx.BITMAP_TYPE_GIF)
    self.panel = wx.Panel(self, pos=wx.Point(100,100), size=wx.Size(400, 400))
    self.bg_bmp = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(self.bg))
    self.sizer.Add(self.panel)

    # Speed Slider
    self.tempo = wx.Slider(self)
    self.sizer.Add(self.tempo, flag=wx.ALIGN_CENTER)

    # Set Layout
    self.SetSizer(self.sizer)
    self.SetAutoLayout(1)
    self.sizer.Fit(self)
    self.Show()

if __name__ == "__main__":
  app = wx.App()
  frame = SimulationApp(None, -1, "Animat Simulation")
  app.MainLoop()