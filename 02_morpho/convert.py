#!/usr/bin/python
# -*- coding: utf-8 -*-

#Conversion MRG

import re
import sys
import fileinput as fi
from optparse import OptionParser

op=OptionParser(usage="""Script de conversion d'un fichier mrg en fichier par colonnes. Réclame du format mrg en entrée et renvoie des paires forme-catégorie, séparées par des tabulations.""")
(op,args)=op.parse_args()

p=re.compile(r"[^() ]+ [^() ]+")
space=re.compile(r"[ ]+")


for mrg in fi.input(args):
	z=mrg.decode("UTF-8")
	for x in p.findall(z):
		tag,word=space.split(x)
		output=word+"\t"+tag
		print output.encode("UTF-8")
