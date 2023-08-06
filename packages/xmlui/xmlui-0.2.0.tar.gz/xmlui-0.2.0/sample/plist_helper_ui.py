#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")

import xmlui
import wx
import os


class PlistDoc:
    def __init__(self, fullname):
        self.fullname = fullname
        self.imagename = self.fullname.replace(".plist", ".png")
        self.image = wx.Image(self.imagename)
        self.bitmap = self.image.ConvertToBitmap()

    def get_image_name(self):
        return self.imagename

class PlistDrawController(xmlui.Controller):
    def __init__(self):
        pass

    def SetDoc(self, doc):
        self.doc = doc
        print("setdoc", doc.fullname)
        self.node.Refresh()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self.node)
        # self.node.PrepareDC(dc)
        # print("draw", self.doc.imagename)
        dc.DrawBitmap(self.doc.bitmap, 0,0)


class MainController(xmlui.Controller):
    def __init__(self):
        self.doc = None

    def after_load(self):
        self.ui_dirtree.ExpandPath(r"D:\zproj\declare_ui\res.plist")
        self.main_frame.Show(True)

    def OnSearch(self, evt):
        print ("onselect", self.ui_dirtree.GetPath())
    def OnCancel(self, evt):
        self.ui_search_file.SetValue("")
    def OnSelectFile(self, evt):
        fname = self.ui_dirtree.GetFilePath().lower()
        if not fname:
            return
        if not os.path.isfile(fname):
            return

        if not fname.endswith(".plist"):
            return

        if self.doc and self.doc.fullname==fname:
            return

        self.doc = PlistDoc(fname)
        self.ui_draw.controller.SetDoc(self.doc)

def main():
    loader = xmlui.XmlWXLoader()
    controllers = [MainController, PlistDrawController]
    wxapp = loader.load("xml_wx.xml", controllers)
    wxapp.MainLoop()

if __name__ == '__main__':
	main()