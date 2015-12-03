#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

class Texte():
  
  def __init__(self):
        self.stringOrig=""
        self.phrases=[]
        
        
  
  def readString(self,string):
    self.stringOrig=string
    phrase=Phrase()
    phrase.identifyWords(string)
    phrase.detectCandidatesEN()
    self.phrases.append(phrase)
    #print self.phrases
    #for ph in self.phrases:
      #ph.printP()
  
  def detectEN(self,string):
    output=""
    self.readString(string)
    for phrase in self.phrases:
      #if phrase.words[0].token=="":
	#return self.stringOrig
      #phrase.printP()
      phrase.searchEN()
      output+=phrase.outputString()
    return output
    
  
    
   

class Phrase():
  
  def __init__(self):
    self.entities=NameEntities()
    self.lengh=0
    self.words=[]
    self.candidatesEN=[]
    
  
  def identifyWords(self, string):
    string=string.split()
    #print string
    i=0
    for w in string:
      #print 
      self.lengh+=1
      el=Word(i)
      el.fromString(w)
      #self.tokens.append(el.token)
      self.words.append(el)
      #print self.tokens
  
  def detectCandidatesEN(self):#cherche les candidat potentiel pour les EN
    for word in self.words:
      if word.token[0].isupper():
	#print word.token
	self.candidatesEN.append(word)
  
  def searchEN(self):
    self.entities.loadDB("04_namedEntity/personne_linking.txt","04_namedEntity/place_linking.txt")
    for word in self.words:
      #print "Londres" in self.entities.places
      if word.token[0].isupper():
	if word.token in self.entities.names:
	  if word.attribut=="":
	    word.attribut='{ORIG=\''+word.token+'\';LIEN=\''+self.entities.names[word.token]+'\'}'
	  else:
	    word.attribut=word.attribut[:-1]+';ORIG=\''+word.token+'\';LIEN=\''+self.entities.names[word.token]+'\'}'
	  word.token='_PERS'
	if word.token in self.entities.places:
	  if word.attribut=="":
	    word.attribut='{ORIG=\''+word.token+'\';LIEN=\''+self.entities.places[word.token]+'\'}'
	  else:
	    word.attribut=word.attribut[:-1]+';ORIG=\''+word.token+'\';LIEN=\''+self.entities.places[word.token]+'\'}'
	  word.token='_LOC'
  
  def outputString(self):
    string=""
    for word in self.words:
      #print word.token
      string+=word.attribut+word.token+" "
    return string
  
  
  def printP(self):
    for word in self.words:
      print word.token


class Word():
  
  def __init__(self,position):
    self.position=position
    self.token=''
    self.attribut=""
  
  def fromString (self, string):
    if "{" in string:
      match=re.search(r'(\{.*\})(.*)', string)
      self.token=match.group(2)
      #print match.group(1)
      self.attribut=match.group(1)
    else:
      self.token=string
      
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
  print txt.detectEN(data)