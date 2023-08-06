#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx
import xml_ui_tool

def get_all_handle_class():
    return {k:v for k,v in globals().items() if type(v)==type}
# def CreateApp(xmlui):
#     parser = xml_ui_tool.ElementParser(HandleCommonTag, xmlui)

#     for parseTagName,parseTagClass in globals().items():
#         if type(parseTagClass)==type:
#             parser.regist_tag_handle(parseTagName, parseTagClass)

#     handle_app = parser.parse(xmlui.xml_root)
#     handle_app.main_frame.Show(True)
#     xmlui.main_frame = handle_app.main_frame
#     return handle_app.custom

class HandleCommonTag(xml_ui_tool.HandleBase):
    def handle_self(self):
        self.custom = self.create_custom()
        if not self.custom:
            self.ui = self.create_ui()

        self.apply_all_attrs()

    def create_custom(self):
        func = getattr(self.parent, self.xml_element.tag, None)
        if not func:
            func = getattr(self, self.xml_element.tag, None)
        if not func and self.parent:
            func = getattr(self.parent.get_result(), self.xml_element.tag, None)

        if not callable(func):
            return

        if not self.xml_element.text.strip():
            func()
        else:
            func(xml_ui_tool.convert_attr_value(self.xml_element.text, {"wx":wx}))

        return True

    def create_ui(self):
        wxClass = getattr(wx, self.xml_element.tag, None)
        if not wxClass:
            return None
        
        ui = wxClass(self.get_latest_ui())

        return ui

    def apply_all_attrs(self):
        label = (self.xml_element.get("label") or self.xml_element.text or "").strip()
        if label and hasattr(self.get_result(), "SetLabel"):
            self.get_result().SetLabel(label)

        for attrName, attrValue in self.xml_element.items():
            func = getattr(self, "apply_attr_"+attrName, None)
            if func:
                func(xml_ui_tool.convert_attr_value(attrValue, {"wx":wx}))
                continue

            func = getattr(self.get_result(), attrName, None)
            if callable(func):
                func(xml_ui_tool.convert_attr_value(attrValue, {"wx":wx}))

    def call_simplefunc_at_result(self, funcName, param):
        func = getattr(self.get_result(), funcName, None)
        if callable(func):
            func(param)

class App(HandleCommonTag):
    def __init__(self):
        self.main_frame = None
    def handle_self(self):
        self.custom = wx.App()
    def after_handle_child(self, child_handle_obj):
        if self.main_frame:
            raise Exception("wx只能有一个主界面")

        if child_handle_obj.ui:
            self.main_frame = child_handle_obj.ui

class BoxSizer(HandleCommonTag):
    def create_custom(self):
        return wx.BoxSizer()

    def handle_over(self):
        stretches = []
        if self.xml_element.get("stretch", "").strip():
            stretches = xml_ui_tool.convert_attr_value(self.xml_element.get("stretch"), {"wx":wx})

        for child in self.children:
            if child.ui:
                stretch = stretches[0] if len(stretches)>0 else 0
                stretches = stretches[1:]
                self.custom.Add(child.ui, stretch, wx.EXPAND)

        self.parent.ui.SetSizer(self.custom)
        self.custom.Fit(self.parent.ui)

class SplitterWindow(HandleCommonTag):
    def SetSashPosition(self, attrValue):
        p1, p2 = self.ui.GetChildren()
        if self.ui.GetSplitMode()==wx.SPLIT_HORIZONTAL:
            self.ui.SplitHorizontally(p1, p2, attrValue)
        elif self.ui.GetSplitMode()==wx.SPLIT_VERTICAL:
            self.ui.SplitVertically(p1, p2, attrValue)

class Bind(HandleCommonTag):
    def handle_self(self):
        bindtype = xml_ui_tool.convert_attr_value(self.xml_element.get("type"), {"wx":wx})
        bindfunc = getattr(self.controller, self.xml_element.text.strip(), None)
        if bindfunc:
            self.parent.ui.Bind(bindtype, bindfunc, self.parent.ui)
