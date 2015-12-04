#!/usr/bin/python
# -*- coding: utf-8 -*-

#Script de créations et de test du perceptron. - Arthur Lapraye - 2015

import math
from optparse import OptionParser
import cPickle as pickle
#from cProfile import run

#Nécessite le fichier morpho.py
from morpho import *

#Fonction pour tester un classifieur
def testit(test,perceptron,matrice=True,LATEX=False):
	if LATEX:
		sep=" & "
		endline="\\\\"
		percentsign="\%"
	else:
		percentsign="%"
		sep="\t"
		endline=" "
	
	wc = 0.0	
	nice = 0.0
	errs = 0.0
	
	realcats = dict(zip(list(cats),(0 for a in list(cats))))
	
	matcon=dict()
	
	for ca1 in cats: 
		for ca2 in cats:
			matcon[ca1,ca2]=0.0
	
	#Création de la matrice de confusion matcon
	for (e,c) in test:
		truecat=c
		realcats[truecat] += 1
		#y=perceptron(getfeatures(e))
		y,z=perceptron(getfeatures(e))[:2]
		matcon[truecat,y] += 1
		if TWO:
			matcon[truecat,z] += 1
			
		#Nice = total des éléments bien catégorisés
		if y == truecat or (TWO and (truecat == z)):
			nice += 1.0
		else:
			errs += 1.0
	
	minimum=None
	#M : option pour afficher la matrice de confusion
	if matrice:
		
		#Les étiquettes de catégories réelles sont affichées à gauches
		#Les étiquettes prédites par l'algorithme sont affichées en haut
		#Il me semble que c'est conventionnel.
		print "Matrice de confusion :"
		z=sorted(cats)
		print sep +sep.join(z) + endline
		
		for ca in z:
			if realcats[ca] != 0 and ((not minimum) or matcon[minimum] > matcon[ca,ca]):
					minimum=(ca,ca)
			
			if realcats[ca] != 0.0:
				if PERCENT:
					p=[str((100*matcon[ca,a])/realcats[ca])[:4]+percentsign+sep for a in z]
				else:
					p=[str(matcon[ca,a]) for a in z]
					
				print ca + sep + "".join(p) + endline
		
	
		print u"Classe la plus mal reconnue :",minimum[0],"précision de :",(100.0*matcon[minimum]/realcats[minimum[0]]),percentsign
	#Calcul de la précision globale : éléments bien catégorisés sur nombre total d'éléments
	p=nice/len(test)
	precision= str(100*p)+"%" if PERCENT else str(nice) + "/" + str(wc)
	print u"Précision globale : " + precision  + "\n"
	
	return p

#Fonction qui extrait et affiche les traits les plus informatifs du vecteur de poids du perceptron
#par catégorie
def meilleurstraits(weight):
	for z in weight:
		feats=(sorted(weight[z],key=lambda x : abs(weight[z][x]),reverse=True))
		print "Meilleur traits pour "+z	
		print "\t"+"\n\t".join([ "\""+x+"\" : "+str(weight[z][x]) for x in feats[:10] ]) + "\n"
		#print "Pire traits pour " + z
		#print "\t"+"\n\t".join([ "\""+x+"\" : "+str(weight[z][x]) for x in feats[-10:] ]) + "\n"

#Fonctions de calcul de distance des vecteurs.
def manhattan(w1,w2):
	return sum([ abs(w1[k]-w2[k]) for k in w1])

def euclide(w1,w2):
	return math.sqrt(sum([ (w1[k]-w2[k])**2 for k in w1]))
	
def distinfini(w1,w2):
	return max([ abs(w1[k]-w2[k]) for k in w1])

#Fonction qui calcule la distance entre les vecteurs de poids associés à différentes catégories
def distweights(weight,MATRICE=True,LATEX=False):
	if LATEX:
		sep=" & "
		endline="\\\\"
		percentsign="\%"
	else:
		percentsign="%"
		sep="\t"
		endline=" "
	
	for (funcname,func) in [("Manhattan",manhattan),("Euclide",euclide),(u"«Infini»",distinfini)]:
		print u"Distance utilisée :",funcname
		if MATRICE:
			print sep+sep.join(weight.keys())+endline
		mini=0
		(min1,min2)=(None,None)
		for z in weight:
			dists=[]
		
			for y in weight:
				p=func(weight[z],weight[y])
				dists.append(p)
				if z != y and (p < mini or mini==0):
					mini=p
					(min1,min2)=(z,y)
			if MATRICE:	
				print z+sep+sep.join([str(int(x)) for x in dists])+" "+endline
		print "Vecteurs les plus proches :",min1,min2
	
if __name__ == "__main__":
	usage=u"""%prog [corpus]
			Programme d'entraînement et de test du perceptron.
			Prend en entrée un corpus de mots présentés sur deux colonnes :
			une colonne de forme et une colonne de catégories gold."""
	p = OptionParser(usage=usage)
	p.add_option("-i","--iteration", action="store",dest="iteration", default=8,
	help=u"Nombres d'itérations du perceptron. Par défaut 8")

	p.add_option("-c", "--confusion",
		              action="store_true", dest="matrice", default=False,
		              help=u"affiche les matrices de confusion")
	
	p.add_option("-t","--test", action="store_true",dest="testit", default=False,
	help=u"""Crée un corpus de test séparé pour tester le perceptron.\n
	Si cette option n'est pas activée, l'entrainement et le test sont menés sur l'intégralité du corpus.""")
	
	p.add_option("-d","--deux",action="store_true",dest="two",default=False,
		help=u"Prendre en compte les deux meilleurs tags lors de l'évaluation")
	
	(op,args)=p.parse_args()
	#Variables globales

	ITER=int(op.iteration)
	MATRICE=op.matrice
	TESTIT=op.testit
	TWO=op.two
	TEST=9
	LATEX=False
	PERCENT=True

	test,train,cats=list(),list(),set()
	for e in args:
		x,y,z=readlexicon(e)
		test += x
		train += y
		cats.update(z)
	
	if not TESTIT:
		train+=test
		test=train
		known=set([e for e,x in test])
		with open("known.pickle","w") as k:
			pickle.dump(known,k)

	print len(cats),"catégories : ",sorted(cats)
	print "taille du corpus d'entraînement : ",len(train)," et du corpus de test : ",len(test)
	print "Entraînement du perceptron :",ITER
	#run("weight=perceptronmaker(cats,train,itermoi=ITER,verbose=False)")
	weight=perceptronmaker(cats,train,itermoi=ITER,verbose=False)

	perceptron=partial(classify,weight)

	testit(test,perceptron,matrice=MATRICE)
	
	if not TESTIT:
		saveweights(weight)

#Kilroy was here

