#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import gobject
import urllib2
import xmltodict
import json
import io
import subprocess

class MetroSTMIndicator:
  def __init__(self):
    self.ind = appindicator.Indicator ("Metro STM Indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_icon("/opt/metro-stm-indicator/0-0-0-0.png")
    #self.ind.set_label("...") 

    # create a menu
    self.menu = gtk.Menu()

    image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    image.connect("activate", self.quit)
    image.show()
    self.menu.append(image)
               
    self.menu.show()

    self.ind.set_menu(self.menu)

    self.metrostatus = {1: False, 2: False, 4: False, 5: False}
    self.metrostatusclear = {1: False, 2: False, 4: False, 5: False}

    # load config
    self.conf = {}
    with io.open('config.json', 'r', encoding='utf-8') as f:
      self.conf = json.load(f)

    self.getETMData()
    gobject.timeout_add(60 * 1000, self.getETMData)

  def quit(self, widget, data=None):
    gtk.main_quit()

  def getETMData(self):
    try:
      print "update"
      ETMfile = urllib2.urlopen('http://www2.stm.info/1997/alertesmetro/esm.xml')
  #    ETMfile = urllib2.urlopen('http://bundesnerdrichtendienst.de/esm.xml')
      ETMdata = ETMfile.read()
      ETMfile.close()
      ETMdata = xmltodict.parse(ETMdata)

      metrostatus = {}
      metromsg = {}
      for i in ETMdata['Root']['Ligne']:
        if i['msgAnglais'] == "Normal métro service.":
          metrostatus[int(i['NoLigne'])] = False
          metromsg[int(i['NoLigne'])] = i['msg' + self.conf['lang']]
        else:
          metrostatus[int(i['NoLigne'])] = True
          metromsg[int(i['NoLigne'])] = i['msg' + self.conf['lang']]

      for i in self.menu.get_children():
        self.menu.remove(i)

      for line, message in metromsg.items():
        self.line = gtk.MenuItem()
        self.line.add(gtk.Label(str(line) + ": " + message))
        self.line.show()
        self.menu.append(self.line)
      self.setIndicator(metrostatus[1], metrostatus[2], metrostatus[4], metrostatus[5])

      if (len(set(metrostatus.items()) & set(self.metrostatus.items())) != 4):
        if (len(set(self.metrostatusclear.items()) & set(metrostatus.items())) == 4):
          subprocess.Popen(["aplay", "timbre3_speciaux_perturbations.wav"])
        else:
          subprocess.Popen(["aplay", "timbre1_clientele.wav"])

      self.metrostatus = metrostatus

    except:
      pass

    return 1

  def setIndicator(self, metro1 = False, metro2 = False, metro4 = False, metro5 = False):
    
    self.ind.set_icon("/opt/metro-stm-indicator/" + str(int(metro1)) + "-" + str(int(metro2)) + "-" + str(int(metro4)) + "-" + str(int(metro5)) + ".png")
    return 0

def main():
  gtk.main()
  return 0

if __name__ == "__main__":
  indicator = MetroSTMIndicator()
  main()
