#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml_ui_tool
import xml_wx
import xml_tk


import xml.etree.ElementTree as ET

class XmlLoader:
    def load(self, file_or_xmlstring, controllers):
        if "<" in file_or_xmlstring or ">" in file_or_xmlstring:
            self.xml_root = ET.fromstring(file_or_xmlstring)
            self.xml_doc = ET.ElementTree(self.xml_root)
        else:
            self.xml_doc = ET.parse(file_or_xmlstring)
            self.xml_root = self.xml_doc.getroot()

        self.controllers = controllers

        return self.parse_root_element()

class XmlWXLoader(XmlLoader):
    def parse_root_element(self):
        parser = xml_ui_tool.DocParser(xml_wx.HandleCommonTag)
        parser.controllers = {clas.__name__:clas for clas in self.controllers}
        parser.handle_class = xml_wx.get_all_handle_class()
        handle_app = parser.parse(self.xml_root)
        return handle_app.get_result()

# class XmlTK(XmlUI):
#     def parse_root_element(self):
#         self.app = xml_tk.CreateApp(self)

#     def mainloop(self):
#         self.app.mainloop()

class Controller:
    def __init__(self):
        self.node = None

    def after_load(self):
        pass

def test_tk():
    import tkinter as tk
    import subprocess

    xmlui = XmlTK()
    xmlui.load(r"C:\Users\23173\Desktop\test\xml_tk.xml")

    version_items = []
    versions = tk.StringVar()
    xmlui.ui_versions["listvariable"] = versions

    def update_version_items():
        del version_items[:]
        res = subprocess.Popen("pyenv versions", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        lines = res.stdout.readlines()
        lines = [x.decode().strip() for x in lines]
        for line in lines:
            if line.startswith("*"):
                version_items.append("*%s"%(line.strip().split()[1]))
            else:
                version_items.append(line.strip())

        versions.set(" ".join(version_items))

    update_version_items()

    def onclick_change():
        sels = xmlui.ui_versions.curselection()
        if len(sels)>0:
            version = version_items[sels[0]]
            version = version.strip()
            os.system("pyenv global %s"%(version))
            os.system("pyenv rehash")
            update_version_items()

    xmlui.ui_change["command"] = onclick_change

    xmlui.mainloop()


if __name__ == '__main__':
    pass
