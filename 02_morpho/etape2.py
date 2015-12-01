#!/usr/bin/python
# -*- coding: utf-8 -*-

import morpho as m
from morpho import defloat
import fileinput as fi
from functools import partial
import re
from optparse import OptionParser

#TODO : meilleurs commentaires
usage="Script pour le pipeline"
p = OptionParser(usage=usage)
p.add_option("-p","--poids",action="store",dest="poids",default="weights.pickle",help="Chemin vers le fichier de poids")
p.add_option("-l","--lexique",action="store",dest="lexique",default="known.pickle",help="Chemin vers le fichier de lexique")

(op,args)=p.parse_args()

FICHIERPOIDS=op.poids
FICHIERLEXIQUE=op.lexique


#Vecteurs de poids du perceptron
w=m.importweights(FICHIERPOIDS)

#Liste de mots connus à ignorer
k=m.importweights(FICHIERLEXIQUE)
k.update(["_HEURE","_HASHTAG","_URL","_DATE","_NOMBRE"])

#Fonction pour récupérer les tags
taggit=m.memoize(lambda x: partial(m.classify,w)(m.getfeatures(x)))

space=re.compile(r" ")

for line in fi.input(args):
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
			
		
 			
		
