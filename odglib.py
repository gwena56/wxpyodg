#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# import
from math import *
import wx
import wx.lib.platebtn as platebtn
from PIL import Image
from PIL import ImageDraw
import ast
import zipfile
import xml.etree.ElementTree as ET
import ConfigParser as ini
from StringIO import StringIO
import uiFunction
# definition variables pour tous les scripts
global ERR_ODG, ERR_SYNTAX, HOVER_MASK, POINT, PLATFORM, CHECK_UPDATE,DO_BUILD,BUILD_NAME
ERR_ODG = "Not a odg file."
ERR_SYNTAX = "Syntax Error"
# préférences standard de certaines variables de l'UI 
PLATFORM = "LINUX" # A CAUSE DE LA COMPATIBILITE DES CHEMIN DE FICHIERS : file path ... LINUX,RASPBERRY_PI,MACOSX,WINDOWS
HOVER_MASK = (255,255,255,255) # couleur des formes autocalculées pour l'hover des boutons
# constant
POINT = 0.03527777777778
# GLOBAL
global file, odg, ptr, data, root, uiPage, Example, window, background, config,iniParams, uiObjects
#def
def S2P(a):
    global POINT
    return int(round(float(a[0:-2])/POINT)) #-2 enleve la mesure cm
def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result
# CLASS
class odgSrc:
    """odgScr"""
    def __init__(self):
        self.data=[]
        self.uiPage ={}
        self.iniObjects={}
        self.uiObjects = {}
        self.uiItems =  []
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
        
    def setParams(self,txt):
        global HOVER_MASK, PLATFORM
        """"setObjects"""
        config = ini.ConfigParser()
        config.read(txt)
        sections = config.sections()
        print sections
        ph =""
        for section in sections:
            ph += "'"+section.upper()+"' :{"
            params = config.options(section)
            for param in params:
                val = config.get(section,param)
                ph += "'"+ param.upper() + "' : '"+val+"',"
            ph+= "} , "
        ph = "{"+ph[0:-1]+"}"
        self.iniParams = dict(ast.literal_eval(ph))
        # definiton de paramètres importants
        try :
            HOVER_MASK = eval(self.iniParams['UI']['HOVER_MASK'])
            PLATFORM = self.iniParams['GENERAL']['PLATFORM']
        except KeyError:
            """RIEN"""
        return self.iniParams
    
    def drawBackgroundIO(self,ou,path):
        """drawBackground"""
        image_data = self.odg.read(path)
        fh = StringIO(image_data)
        img=wx.ImageFromStream(fh, wx.BITMAP_TYPE_ANY )
        bitmap = wx.BitmapFromImage(img)
        bitmap = scale_bitmap(bitmap, self.uiPage['width'], self.uiPage['height'])
        control = wx.StaticBitmap(ou, -1, bitmap)
        
    def page(self):
        for self.ptr in self.root.iter('{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}page'):
            page = self.ptr[0].attrib
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
                #recupération du bloc objet de odg
                y = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}y'])
                x = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}x'])
                width = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width'])
                height = S2P(object['{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height'])
                object = self.ptr[i].tag
                temp = "{'x':'"+str(x)+"','y':'" +str(y)+"','width':'"+str(width)+"','height':'"+str(height)+"'"
                #calcul du type d'objet
                typeObject = object.replace("urn:oasis:names:tc:opendocument:xmlns:drawing:1.0","")[2:]
                temp += ",'typeObject':'"+typeObject+"'"
                if typeObject == "circle" or typeObject == "ellipse":
                    typeObject = "ellipse"
                    nom = self.ptr[i][0][0].text
                    try :
                        action = self.ptr[i][1][0].text
                    except IndexError:
                        action ="none"
                    temp += ",'action':'"+action+"'"
                    self.uiObjects[nom] = dict(ast.literal_eval(temp + "}"))
                if typeObject == "frame":
                    h = self.ptr[i][0].attrib
                    image = h['{http://www.w3.org/1999/xlink}href']
                    self.odg.extract(image,'./ui')
                    nom = self.ptr[i][0][0][0].text
                    temp += ",'image':'"+image+"'"
                    self.uiObjects[nom] = dict(ast.literal_eval(temp + "}"))
                if typeObject == "custom-shape":
                    nom = self.ptr[i][0][0].text
                    self.uiObjects[nom] = dict(ast.literal_eval(temp + "}"))
        except IndexError:
            """PPP"""
        return self.uiPage
    
    def CreateHoverPng(self,nom,x,y,width,height):
        # on précise les global nécéssaires -> c'est surtout des variables du .ini
        global HOVER_MASK
        #print nom,x,y,width,height
        img = Image.open("./ui/Pictures/background.png")
        #bb = (int(x),int(y),int(width),int(height))
        crop_rectangle = (int(x),int(y),int(x)+int(width)+2,int(y)+int(height)+2)
        cropped_im = img.crop(crop_rectangle)#.convert('RGBA')
        cropped_im.save("./ui/Pictures/"+nom+".png")
        poly = Image.new('RGBA', cropped_im.size)
        pdraw = ImageDraw.Draw(poly)
        bb = (0,0,int(width),int(height))
        pdraw.ellipse(bb, fill = HOVER_MASK) #(255,255,255,84)
        cropped_im.paste(poly,mask=poly)
        cropped_im.save("./ui/Pictures/"+nom+"_hover.png")
        
#### defS utilisant wxPython
    def uiMake(self):
        """Example STD_PUSHBT_ONOFF -> 
        STD_=standard item, 
        PUSHBT_ = this is a push button
        ONOFF = it's name"""
        for uiObject in self.uiObjects.keys():
            obj = self.uiObjects[uiObject]
            nom = uiObject.split("_")
            if nom[1]=="PUSHBT":
                self.pushbutton(obj,nom)
                
    def pushbutton(self,obj,nom):
        """bouton poussoir"""
        if nom[0]=="STD":
           self.CreateHoverPng(nom[2],obj['x'],obj['y'],obj['width'],obj['height'])
           nImg = wx.Image("./ui/Pictures/"+nom[2]+".png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
           hImg = wx.Image("./ui/Pictures/"+nom[2]+"_hover.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
           #(int(obj['x']),int(obj['y'])),(int(obj['width']),int(obj['height']))
           #, style=wx.BU_AUTODRAW|wx.NO_BORDER 
           vars()[nom[2]] = wx.BitmapButton(self.appBackground, -1, nImg,(int(obj['x'])-1,int(obj['y'])-1), (int(obj['width']),int(obj['height'])), style=wx.BU_AUTODRAW|wx.NO_BORDER)
           vars()[nom[2]].SetBitmap(nImg)
           vars()[nom[2]].SetBitmapSelected(nImg)
           vars()[nom[2]].SetBitmapHover(hImg)
        elif nom[0]=="BP":
            """NOP"""
        else :
            """ Draw RED X ON IMAGE BLOC """

    def drawBackground(self,ou,path):
        """drawBackground"""
        img=wx.Image('./ui/'+self.uiPage['image'], wx.BITMAP_TYPE_ANY)
        bitmap = wx.BitmapFromImage(img)
        bitmap = scale_bitmap(bitmap, self.uiPage['width'], self.uiPage['height'])
        control = wx.StaticBitmap(ou, -1, bitmap)
        # save du fichier Background pour création des autres éléments
        img=bitmap.ConvertToImage()
        img.SaveFile("./ui/Pictures/background.png", wx.BITMAP_TYPE_PNG)
        
    def initUI(self):
        self.page()
        self.window = wx.Frame(None, style= wx.FULL_REPAINT_ON_RESIZE | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX) 
        self.window.SetSize((self.uiPage['width'],self.uiPage['height']+20))
        self.appBackground = wx.Panel(self.window, -1)
        self.drawBackground(self.appBackground,self.uiPage['image'])
        self.uiMake()
        print PLATFORM