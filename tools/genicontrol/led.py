#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## LED control taken from http://code.activestate.com/recipes/533125-wxpython-led-control/.
##

import wx

def change_intensity(color, fac):
    rgb = [color.Red(), color.Green(), color.Blue()]
    for i, intensity in enumerate(rgb):
        rgb[i] = min(int(round(intensity*fac, 0)), 255)

    return wx.Color(*rgb)

class LED(wx.Control):
    def __init__(self, parent, id = -1, colors = [wx.Colour(220, 10, 10), wx.Colour(250, 200, 0), wx.Colour(10, 220, 10)],
                 pos = (-1, -1), style = wx.NO_BORDER):
        size = (17, 17)
        wx.Control.__init__(self, parent, id, pos, size, style)
        self.MinSize = size

        self._colors = colors
        self._state = -1
        self.SetState(0)
        self.Bind(wx.EVT_PAINT, self.OnPaint, self)

    def SetState(self, i):
        if i < 0:
            raise ValueError, 'Cannot have a negative state value.'
        elif i >= len(self._colors):
            raise IndexError, 'There is no state with an index of %d.' % i
        elif i == self._state:
            return

        self._state = i
        base_color = self._colors[i]
        light_color = change_intensity(base_color, 1.15)
        shadow_color = change_intensity(base_color, 1.07)
        highlight_color = change_intensity(base_color, 1.25)

        ascii_led = '''
        000000-----000000
        0000---------0000
        000-----------000
        00-----XXX----=00
        0----XX**XXX-===0
        0---X***XXXXX===0
        ----X**XXXXXX====
        ---X**XXXXXXXX===
        ---XXXXXXXXXXX===
        ---XXXXXXXXXXX===
        ----XXXXXXXXX====
        0---XXXXXXXXX===0
        0---=XXXXXXX====0
        00=====XXX=====00
        000===========000
        0000=========0000
        000000=====000000
        '''.strip()

        xpm = ['17 17 5 1', # width height ncolors chars_per_pixel
               '0 c None',
               'X c %s' % base_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii'),
               '- c %s' % light_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii'),
               '= c %s' % shadow_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii'),
               '* c %s' % highlight_color.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii')]

        xpm += [s.strip() for s in ascii_led.splitlines()]

        self.bmp = wx.BitmapFromXPMData(xpm)

        self.Refresh()

    def GetState(self):
        return self._state

    State = property(GetState, SetState)

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)

from random import randrange

class LcdTest(wx.Frame):
    def __init__(self):
        super(LcdTest, self).__init__(None, size=(200,200))

        self._p = wx.Panel(self)

        colors = [wx.Color(128, 128, 128), wx.Color(192, 0, 0), wx.Color(0, 192, 0), wx.Color(0, 0, 192), ]
        l1 = LED(self._p, colors = colors)
        l2 = LED(self._p, colors = colors)
        l3 = LED(self._p, colors = colors)
        self._led_lst = (l1, l2, l3)

        sz = wx.BoxSizer(wx.VERTICAL)
        flg = wx.ALL | wx.ALIGN_CENTER
        sz.Add(l1, 0, flg, 5)
        sz.Add(l2, 0, flg, 5)
        sz.Add(l3, 0, flg, 5)

        self._p.SetSizerAndFit(sz)
        self.SetClientSize(sz.GetSize())
        self.Show()

        wx.FutureCall(125, self._time_passed)

    def _time_passed(self):
        lcd_work = self._led_lst[ randrange(0, 3) ]
        lcd_work.SetState( randrange(0, 4) )

        wx.FutureCall(500, self._time_passed)

def main():
    app = wx.PySimpleApp()
    f = LcdTest()
    app.MainLoop()

if __name__ == "__main__":
    main()

    """
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()

def bitmap1_onSize(self, e=None):
    W, H = self.bitmap1.Size
    if W > H:
        NewW = W
        NewH = W * H / W
    else:
        NewH = H
        NewW = H * W / H
    img = wx.Image(self.frame_file_picker.Path, wx.BITMAP_TYPE_ANY)
    img = img.Scale(NewW,NewH)
    self.bitmap1.SetBitmap(wx.BitmapFromImage(img))
    e.Skip()
    """
