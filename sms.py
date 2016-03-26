#!/usr/bin/python
# -*- coding: utf-8 -*-
from odglib import *
import argparse
import wx
odg = odgSrc()
odg.setUI("./odg/field.odg") #set User Interface from odg file
odg.setParams("carpc.ini")# un petit peu de prefs !!
odg.screen = wx.App()
odg.initUI() # on lance interface utilisateur
odg.window.Centre() #on centre la fenetre principale
odg.window.Show(True)#on affiche tout
odg.screen.MainLoop()
# et c'est tout !!!'
