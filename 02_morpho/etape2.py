#!/usr/bin/python
# -*- coding: utf-8 -*-

import morpho as m
from morpho import defloat
import fileinput as fi
from functools import partial
import re
from optparse import OptionParser
import sys

#TODO : meilleurs commentaires
usage=u"""%prog lignes [-p poids] [-l lexique] 
	Script pour le pipeline. Utilise un fichier de vecteur de poids et un fichier de lexique.
	Étiquette les mots inconnus sur une ligne. Prend en entrée un fichier ou stdin.
	"cat fichier" | %prog et "%prog fichier" sont équivalents.
	Par défaut le fichier de poids et le fichier de lexique sont weights.pickle et known.pickle 
	dans le répertoire d'exécution, sinon ils doivent être spécifiés en option."""

p = OptionParser(usage=usage)
p.add_option("-p","--poids",action="store",dest="poids",default="weights.pickle",help="Chemin vers le fichier de poids")
p.add_option("-l","--lexique",action="store",dest="lexique",default="known.pickle",help="Chemin vers le fichier de lexique")

(op,args)=p.parse_args()

FICHIERPOIDS=op.poids
FICHIERLEXIQUE=op.lexique


#Vecteurs de poids du perceptron
w=m.importpickle(FICHIERPOIDS)

#Liste de mots connus à ignorer
k=m.importpickle(FICHIERLEXIQUE)
k.update(["_HEURE","_HASHTAG","_URL","_DATE","_NOMBRE"])

#Fonction pour récupérer les tags
taggit=m.memoize(lambda x: partial(m.classify,w)(m.getfeatures(x)))

#space=re.compile(r" ")

#def gettokens(line):

for line in fi.input(args):
	line=line.decode("utf-8")
	for x,y,z in re.findall(r"(\{[^\}]+\})?(\S+)(\s+)",line):
		tag=taggit(y)
		if y not in k and y.lower() not in k:
			if len(x) != 0:
				x=x[:-1]+"TMP_TAG='" + ",".join(map(str,tag)) + "';}"
			else:
				x="{TMP_TAG='" + ",".join(map(str,tag)) + "';}"
		
		out=x+y+z
		sys.stdout.write(out.encode("utf-8"))


