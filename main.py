#!/usr/bin/python
# -*- coding: utf-8 -*-
from odglib import *
import argparse
import wx
odg = odgSrc()
odg.setUI("carpc.odg") #set User Interface from odg file
odg.setParams("carpc.ini") # set User interface UI,GENERAL params such HOVER_MASK color
app = wx.App() # on garde un peu de controle sur l'app
odg.initUI() # on lance interface utilisateur
odg.window.Centre() #on centre la fenetre principale
odg.window.Show(True)#on affiche tout
app.MainLoop()
# et c'est tout !!!