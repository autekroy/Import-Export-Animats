import wx

app = wx.App(False)

frame = wx.Frame(None, title="Draw on Panel")
panel = wx.Panel(frame)

def on_paint(event):
    dc = wx.PaintDC(event.GetEventObject())
    dc.Clear()
    dc.SetPen(wx.Pen("BLACK", 4))
    dc.DrawCircle(100, 100, 50)

panel.Bind(wx.EVT_PAINT, on_paint)

frame.Show(True)
app.MainLoop()