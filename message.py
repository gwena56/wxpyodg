#!/usr/bin/python
# -*- coding: utf-8 -*-
from odglib import *
import argparse
import wx
# arguments possibles
# --text -t
# --font -f
# --color -c 000000 web format without #
# --sqlite file
# --web (html as text)
parser = argparse.ArgumentParser()
parser.add_argument("-t","--text",default ="Default message.py.", help="text to be show in message screen")
parser.add_argument("-s","--size", help="text size in message screen")
parser.add_argument("-f","--font", help="text font. default is one system font")
parser.add_argument("-c","--color", help="color font web code only at the moment without ######.")
parser.add_argument("--sqlite", help="local sqlite request on os_message.sql3 base. NOT IMPLEMENTED YET")
parser.add_argument("--web", help="web adress result. html as text.  NOT IMPLEMENTED YET")
args = parser.parse_args()
############
odg = odgSrc()
odg.setUI("./odg/message.odg") #set User Interface from odg file
odg.setParams("carpc.ini")# un peu de prefs...!!
odg.screen = wx.App() # on garde un peu de controle sur l'app
# gestion des parametres du script
if args.font:
    odg.FONT=args.font
if args.size:
    odg.SIZE=int(args.size)
if args.color:
    odg.FONTCOLOR= odg.HTMLColorToRGB(args.color)
if args.text:
    odg.TEXT = args.text
odg.initUI() # on lance interface utilisateur
odg.window.Centre() #on centre la fenetre principale
odg.window.Show(True)#on affiche tout
odg.screen.MainLoop()
# et c'est tout !!!'