#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

class Texte():
  
  def __init__(self):
        self.stringOrig=""
        self.phrases=[]
        
        
  
  def readString(self,data):
    for string in data:
      phrase=Phrase()
      phrase.identifyWords(string)
      self.phrases.append(phrase)
  
  def detectEN(self,string):
    output=""
    self.readString(string)
    for phrase in self.phrases:
      #if phrase.words[0].token=="":
	#return self.stringOrig
      #phrase.printP()
      phrase.searchEN()
      output+=phrase.outputString()+'\n'
    return output
    
  
    
   

class Phrase():
  
  def __init__(self):
    self.entities=NameEntities()
    self.lengh=0
    self.words=[]
    self.string=""
    self.candidates=[]
    self.tokens=[]
    
  
  def identifyWords(self, string):
    string=self.checkSplit(string.split())
    i=0
    for w in string:
      self.lengh+=1
      el=Word(i)
      el.fromString(w)
      self.tokens.append(el.token)
      self.words.append(el)
      self.string+=el.token+" "
    #print self.string
  
  def checkSplit(self, split2check):#pour eviter le split sur des espaces entre les "{}"
    for el in split2check:
      if "{" in el and "}" not in el:
	index=split2check.index(el)
	i=index+1
	toConcaten=split2check[index+1]
	if "}" not in toConcaten:
	  while "}" not in toConcaten:
	    el+=" "+toConcaten
	    split2check[index]=el
	    del(split2check[index+1])
	    toConcaten=split2check[index+1]
	  el+=" "+toConcaten
	  split2check[index]=el
	  del(split2check[index+1])
	else:
	  el+=" "+toConcaten
	  split2check[index]=el
	  del(split2check[index+1])
    return split2check
	
	  
  
  def detectCandidatesEN(self):#cherche les candidats potentiels pour les EN
    #print "str", self.string
    candidatesEN=[]
    #match=re.findall(r"((?:[A-Z](?:\.|\w*)\s(?:(?:de|du|le|von|van)\s)?(?:(?:[A-Z]+(?:[a-z]+)?)\s)))|([A-Z]\w*\s)|", self.string)
    self.candidates=re.findall(r"((?:\b[A-Z]\w*)(?:\s|-)(?:[A-Z]\w*\s)*|(?:\b[A-Z]\w*\s))", self.string)
    for i in xrange(len(self.candidates)):
      self.candidates[i]=self.candidates[i][:-1]
    #print "yeees", self.candidates
    
    
  def searchEN(self):
    #self.entities.loadDB("04_namedEntity/Pers.txt","04_namedEntity/Loc.txt", "04_namedEntity/Orgs.txt")
    self.entities.loadDB("04_namedEntity/Pers.txt","04_namedEntity/Pers_var.txt", "04_namedEntity/Loc.txt", "04_namedEntity/Orgs.txt")
    self.search_ruleBased_EN()
    self.detectCandidatesEN()
    #print 'Cand', self.candidates
    for word in self.candidates:
	#print 'word', word
	if word in self.entities.names and word!="Les" and word!="Le":
	  #print 'YEEEEH'
	  properName=self.entities.names[word]
	  #print word, properName
	  self.fusion_des_tokens(word,'_PERS',self.entities.namesLink[word])
	if word in self.entities.places:
	  self.fusion_des_tokens(word,'_LOC',self.entities.places[word])
	if word in self.entities.orgs:
	  self.fusion_des_tokens(word,'_ORG',self.entities.orgs[word]) 
  
  def fusion_des_tokens(self, tokenAfusionner,etiquette,lien):
    split=tokenAfusionner.split()
    if len(split)==1:
      index=self.tokens.index(tokenAfusionner)
      if self.words[index].attribut=="":
	    self.words[index].attribut='{ORIG=\''+tokenAfusionner+'\';LIEN=\''+lien+'\';}'
      else:
	    attributNouv=self.words[index].attribut[:-1]+'ORIG=\''+tokenAfusionner+'\';LIEN=\''+lien+'\';}'
	    self.words[index].attribut=attributNouv
      self.words[index].token=etiquette
    else:
      lenth=len(split)
      index=self.tokens.index(split[0])
      if self.words[index].attribut=="":
	    self.words[index].attribut='{ORIG=\''+tokenAfusionner+'\';LIEN=\''+lien+'\';}'
      else:
	    attributNouv=self.words[index].attribut[:-1]+'ORIG=\''+tokenAfusionner+'\';LIEN=\''+lien+'\';}'
	    self.words[index].attribut=attributNouv
      self.words[index].token=etiquette
      for i in xrange(index+1,index+lenth):
	if self.words[i].attribut!='':
	  attributNouv=self.words[index].attribut[:-1]+self.words[i].attribut[1:]
	  self.words[index].attribut=attributNouv
      i=1
      while i<lenth:
	i+=1	
	del(self.words[index+1])
      
      #actualisation self.string
      self.string=""
      self.tokens=[]
      for w in self.words:
	self.tokens.append(w.token)
	self.string+=w.token+" "
  

  #def searchEN(self):
    #self.entities.loadDB("04_namedEntity/Pers.txt","04_namedEntity/Pers_var.txt", "04_namedEntity/Loc.txt", "04_namedEntity/Orgs.txt")
    ##self.entities.loadDB("Pers.txt","Pers_var.txt", "Loc.txt", "Orgs.txt")
    #self.search_ruleBased_EN()
    #self.detectCandidatesEN()
    #for word in self.words:
      #if len(word.token)>0 and word.token[0].isupper():
	#if word.token in self.entities.names:
	  #properName=self.entities.names[word.token]
	  #if word.attribut=="":
	    #word.attribut='{ORIG=\''+word.token+'\';LIEN=\''+self.entities.namesLink[properName]+'\'}'
	  #else:
	    #word.attribut=word.attribut[:-1]+';ORIG=\''+word.token+'\';LIEN=\''+self.entities.namesLink[properName]+'\'}'
	  #word.token='_PERS'
	#if word.token in self.entities.places:
	  #if word.attribut=="":
	    #word.attribut='{ORIG=\''+word.token+'\';LIEN=\''+self.entities.places[word.token]+'\';}'
	  #else:
	    #word.attribut=word.attribut[:-1]+';ORIG=\''+word.token+'\';LIEN=\''+self.entities.places[word.token]+'\'}'
	  #word.token='_LOC'
  
  def search_ruleBased_EN(self):
    if re.search(r"\b(M.|Mme|Mlle)\b", self.string):
      match=re.search(r"(M.|Mme|Mlle)\s?(\b[A-Z]\w+)\s?((?:de|von|le)?\s?[A-Z]\w+)?",self.string)
      ne = match.group(0)
      ne_len=len(ne.split())
      string_lst=self.string.split()
      pattern=re.search("(M.|Mme|Mlle)", self.string)
      index=string_lst.index(pattern.groups(0)[0])
      if self.words[index].attribut=="":
	    self.words[index].attribut='{ORIG=\''+ne+'\'}'
      else:
	    self.words[index].attribut[:-1]+=';ORIG=\''+ne+'\'}'
      self.words[index].token='_PERS'
      for i in xrange(index+1,index+ne_len):
	if self.words[i].attribut!='':
	  self.words[index].attribut[:-1]+=self.words[i].attribut[1:]
      i=1
      while i<ne_len:
	i+=1	
	del(self.words[index+1])
      self.string=""
      self.tokens=[]
      for w in self.words:
	self.tokens.append(w.token)
	self.string+=w.token+" "
      
  
  def outputString(self):
    string=""
    for word in self.words:
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
      if match==None:
	self.token=" "
	self.attribut="{}"
      else:
	self.token=match.group(2)
	self.attribut=match.group(1)
    else:
      self.token=string
      
class NameEntities():
  
  def __init__(self):
        self.names={}
        self.namesLink={}
        self.places={}
        self.orgs={}
  
  def loadDB(self, dicPersLink, dicPersVariants, dicLieux, dicOrgs):
	
	file=open(dicPersLink)
	line=file.readline()
	while line<>"":
	  line=line.split('\t')
	  newLine=[]
	  self.namesLink[line[0]]=line[1][:-1]
	  line=file.readline()
	#print self.names
	file.close()
	
	file=open(dicPersVariants)
	line=file.readline()
	while line<>"":
	  line=line.split('\t')
	  newLine=[]
	  self.names[line[0]]=line[1][:-1]
	  line=file.readline()
	#print "Yes", "René" in self.names
	file.close()
	
	file=open(dicLieux)
	line=file.readline()
	while line<>"":
	  line=line.split('\t')
	  self.places[line[0]]=line[1][:-1]
	  line=file.readline()
	#print self.places
	file.close()   
	
	file=open(dicOrgs)
	line=file.readline()
	while line<>"":
	  line=line.split('\t')
	  self.orgs[line[0]]=line[1][:-1]
	  line=file.readline()
	#print self.places
	file.close() 
      
      
if __name__ == '__main__':
  data=sys.stdin.readlines()
  txt=Texte()
  #print data
  print txt.detectEN(data)