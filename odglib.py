#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# import
from math import *
import wx
import wx.lib.platebtn as platebtn
from PIL import Image
import ast
import zipfile
import xml.etree.ElementTree as ET
import ConfigParser as ini
from StringIO import StringIO
# definition variables pour tous les scripts
ERR_ODG = "Not a odg file."
ERR_SYNTAX = "Syntax Error"
# constant
POINT = 0.03527777777778
# GLOABAL
global file, odg, ptr, data, root, uiPage, Example, window, background, config,iniObjects, uiObjects
#def
def S2P(a):
    return round(float(a[0:-2])/POINT) #-2 enleve la mesure cm
def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result
#CLASS

class odgSrc:
    """AZER"""
    def __init__(self):
        self.data=[]
        self.uiPage ={}
        self.uiObjects = {}
    def setUI(self,txt):
        self.odg = zipfile.ZipFile(txt, "r")
        for filename in ['content.xml']:
            try:
                data = self.odg.read(filename)
        #print data
            except KeyError:
                print ERR_ODG
            else:
                self.root = ET.fromstring(data)
            return self.root
    def uiMake(self):
        """uiMake"""

              
    def setObjects(self,txt):
        """"AZER"""
        config = ini.ConfigParser()
        config.read(txt)
        Objects = config.sections()
        ph =""
        for object in Objects:
            ph += "'"+object+"' :{"
            options = config.options(object)
            for option in options:
                val = config.get(object,option)
                ph += "'"+ option + "' : '"+val+"',"
            ph+= "} , "
        
        ph = "{"+ph[0:-1]+"}"
        #print ph
        self.iniObjects = dict(ast.literal_eval(ph))
        return self.iniObjects
    
    def drawBackgroundIO(self,ou,path):
        """drawBackground"""
        image_data = self.odg.read(path)
        fh = StringIO(image_data)
        img=wx.ImageFromStream(fh, wx.BITMAP_TYPE_ANY )
        bitmap = wx.BitmapFromImage(img)
        bitmap = scale_bitmap(bitmap, self.uiPage['width'], self.uiPage['height'])
        control = wx.StaticBitmap(ou, -1, bitmap)
        
    def drawBackground(self,ou,path):
        """drawBackground"""
        #image_data = self.odg.read(path)
        #fh = StringIO(image_data)
        #img=wx.ImageFromStream(fh, wx.BITMAP_TYPE_ANY )
        img=wx.Image('./ui/'+self.uiPage['image'], wx.BITMAP_TYPE_ANY)
        bitmap = wx.BitmapFromImage(img)
        bitmap = scale_bitmap(bitmap, self.uiPage['width'], self.uiPage['height'])
        control = wx.StaticBitmap(ou, -1, bitmap)

    def page(self):
        for self.ptr in self.root.iter('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}page'):
            page = self.ptr[0].attrib
            #self.uiPage['y'] = int(page['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y'][0:-2])
        self.uiPage['y'] = S2P(page['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y'])
        self.uiPage['x'] = S2P(page['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x'])
        self.uiPage['width'] = S2P(page['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width'])
        self.uiPage['height'] = S2P(page['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height'])
        image = self.ptr[0][0].attrib
        self.uiPage['image'] = image['{http://www.w3.org/1999/xlink}href']
        self.odg.extract(self.uiPage['image'], './ui') #extration du fichier background dans user interface
        try : # interprétation du code et définition de chaque objet de l'UI
            for i in range(1,20) :
                xml = self.ptr[i] 
                object = self.ptr[i].attrib
                y = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y'])
                x = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x'])
                width = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width'])
                height = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height'])
                object = self.ptr[i][0].text
                print xml;object
                print
        except:
            """nop"""
        return self.uiPage
    def button(self):
        """boutons"""
    def toggle(self):
        """toggle"""
#### defS utilisant wxPython
    def initUI(self):
        self.page()
        self.window = wx.Frame(None, style= wx.FULL_REPAINT_ON_RESIZE | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX) 
        self.window.SetSize((self.uiPage['width'],self.uiPage['height']+20))
        fond = wx.Panel(self.window, -1)
        self.drawBackground(fond,self.uiPage['image'])
        btn = platebtn.PlateButton(fond, label="", style=platebtn.PB_STYLE_NOBG)
        btn.SetLabelColor(wx.BLUE, wx.BLUE)
        self.window.Centre()
        self.window.Show(True)