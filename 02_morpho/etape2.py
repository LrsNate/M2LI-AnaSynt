#!/usr/bin/python
# -*- coding: utf-8 -*-

import morpho as m
from morpho import defloat
import fileinput as fi
from functools import partial
import re

#Vecteurs de poids du perceptron
w=m.importweights("weights.pickle")

#Liste de mots connus à ignorer
k=m.importweights("known.pickle")
k.update(["_HEURE","_HASHTAG","_URL","_DATE","_NOMBRE"])

#Fonction pour récupérer les tags
taggit=m.memoize(lambda x: partial(m.classify,w)(m.getfeatures(x)))

space=re.compile(r" ")

for line in fi.input():
	concat=str()
	line=line.decode("utf-8")
	line=line.strip()
	lines=space.split(line)
	
	if "" in lines:
		lines.remove("")
	
	for e in lines:
		a=" "
		if e[0]=="{":
			z=e.index("}")+1
			a,b=e[:z],e[z:]
			word=b
		else:
			word=e
			
		word=word.strip()
		
		if word=="":
			print "'",e,"'"
		
		
		if word not in k:
			#print line,taggit(line.decode("utf-8"))
			if a[0] == "{":
				a=a[:-1]
			else:
				a="{"
			
			concat +=  a + "TMP_TAG='" + ",".join(map(str,taggit(word))) + "';}" +word + " "
		else:
			if a[0] == "{":
				concat += a + word + " "
			else:
				concat += word + " "
	
	print concat
			
		
 			
		
