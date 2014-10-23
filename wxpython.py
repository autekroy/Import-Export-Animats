#!/usr/bin/python
import animats

try:
  import wx
except ImportError:
  raise ImportError, "wxPython is required to run this application"

class SimulationApp(wx.Frame):
  def __init__(self, parent, id, title, env):
    wx.Frame.__init__(self, parent, id, title)
    self.env = env
    self.parent = parent
    self.initialize()

  def initialize(self):
    # Grid layout
    self.sizer = wx.BoxSizer(wx.VERTICAL)

    # Background image
    self.panel = wx.Panel(self, pos=wx.Point(100,100), size=wx.Size(400, 400))
    self.panel.Bind(wx.EVT_PAINT, self.on_paint)
    self.sizer.Add(self.panel)

    # TODO - Get bitmap background on panel
    # self.bg = wx.Image('bg.gif', wx.BITMAP_TYPE_GIF)
    # self.bg_bmp = wx.StaticBitmap(self.panel, 1, wx.BitmapFromImage(self.bg))

    # Speed Slider
    self.tempo = wx.Slider(self)
    self.sizer.Add(self.tempo, flag=wx.ALIGN_CENTER)

    # Set Layout
    self.SetSizer(self.sizer)
    self.SetAutoLayout(1)
    self.sizer.Fit(self)
    self.Show()

  def on_paint(self, event):
      dc = wx.PaintDC(event.GetEventObject())
      dc.Clear()
      dc.SetPen(wx.Pen("BLACK", 4))
      for animat in self.env.animats:
        dc.DrawCircle(animat.x, animat.y, 10)
      self.env.update()
      # TODO - Get the app to repaint continuously
      

if __name__ == "__main__":
  app = wx.App()
  frame = SimulationApp(None, -1, "Animat Simulation", animats.Environment(5))
  app.MainLoop()