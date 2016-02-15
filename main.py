#!/usr/bin/python
# -*- coding: utf-8 -*-
from odglib import *
import argparse
import wx
odg = odgSrc()
odg.setUI("alarme.odg") #set User Interface from odg file
#odg.setObjects("carpc.ini") # set User interface Command from ini file
app = wx.App() # on garde un peu de controle sur l'app
odg.initUI() # on lance interface utilisateur
odg.window.Centre() #on centre la fenetre principale
odg.window.Show(True)#on affiche tout
app.MainLoop()
# et c'est tout !!!'