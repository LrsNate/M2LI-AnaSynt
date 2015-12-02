#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

class Texte():
  
  def __init__(self):
        self.string2Analyse=""
        self.stringOriginal=""
        self.entities=NameEntities()
  
  def readString(self,string):
    self.stringOriginal=string
    self.string2Analyse=re.sub(r'\{(.+?)\}', '', string)
    #print self.string2Analyse
  
  def detectEntity(self,string):
    self.entities.loadDB("persons.txt", "places.txt")
    self.readString(string)
    text=self.string2Analyse.split()
    output=""
    #print 'text',text
    for word in text:
      if word in self.entities.names:
	#orig=word
	match=re.search(r"(.*)%s(.*)" % word, self.stringOriginal)
	entityOut='{ORIG=\"'+word+'\", LIEN=\" '+ self.entities.names[word]+'\"}_PERS'
	output = match.group(1)+entityOut+match.group(2)
	self.stringOriginal=output
      elif word in self.entities.places:
	orig=word
	match=re.search(r"(.*)%s(.*)" % word, self.stringOriginal)
	entityOut='{ORIG=\"'+word+'\", LIEN=\" '+ self.entities.places[word]+'\"}_LOC'
	output = match.group(1)+entityOut+match.group(2)
	self.stringOriginal=output
      #if word in entities.orgs:
	#name='_ORG'
	#orig=word
    return self.stringOriginal
	
    
    
class NameEntities():
  
  def __init__(self):
        self.names={}
        self.places={}
        self.orgs={}
  
  def loadDB(self, dicPers, dicLieux):
	file=open(dicPers)
	line=file.readline()
	while line<>"":
	  line=line.split('\t')
	  newLine=[]
	  self.names[line[0]]=line[1][:-1]
	  line=file.readline()
	#print self.names
	file.close()
	
	file=open(dicLieux)
	line=file.readline()
	while line<>"":
	  line=line.split('\t')
	  self.places[line[0]]=line[1][:-1]
	  line=file.readline()
	#print self.places
	file.close()
	


      

if __name__ == '__main__':
  data=sys.stdin.readline()
  txt=Texte()
  #print data
  print txt.detectEntity(data)