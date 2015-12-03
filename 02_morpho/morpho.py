#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import random
from functools import partial
from collections import defaultdict
import cPickle as pickle

#Perceptron et fonctions associées - Arthur Lapraye - 2015

#Variables globales
CAPITALES=u'ABCDEFGHIJKLMNOPQRSTUVWXYZÉÈÙÇÀÔÖÎÂÏÛÊËØ'
CLASSESFERMEES= [u'ADJWH']
#CLASSESFERMEES est une liste de catégories qu'on souhaite ignorer. 
#On peut vouloir ignorer la plupart des catégories suivantes :
#[u'P+D',u'P+PRO',u'ADVWH',u'CC',u'CLO',u'CLR',u'CLS',u'CS',u'DET',u'DETWH',u'P',u'PRO',u'PROREL',u'PROWH'] 

#Décorateur pour la mise en cache dans un dictionnaire de résultats de l'appel à une fonction
#Permet de limiter les appels à des fonctions couteuses en temps de calcul
#Cette technique de mémoisation est assez rudimentaire, elle ne fonctionne que pour les fonctions d'un seul argument
#En outre, l'argument de la fonction doit pouvoir servir de clef à un dictionnaire
#Autrement dit, il ne doit pas appartenir à un type mutable
def memoize(f):
	memo = {}
	def helper(x):
		if x not in memo:			
			memo[x] = f(x)
		return memo[x]
	return helper


#Fonction de lecture de corpus : prend un nom de fichier contenant des exemples
#Renvoie deux listes, train et test, de tuples (forme, catégorie), plus la liste des catégories relevées dans le fichier
#La variable TEST sert à constituer un corpus de test.
def readlexicon(fichier,TEST=9):
	
	#Compiler les regexp octroie un léger gain de temps
	tabz=re.compile(r"\t")
	
	train,test=list(),list()
	
	#Pour chaque mot, la variable c est tirée au hasard entre 0 et TEST inclus
	#Si c == TEST, alors la variable fait partie du corpus de test
	#Quand TEST==9, Environ 90% du corpus sert à l'entraînement et 10% au test.
	c=random.randint(0,TEST)
	
	#Ensemble des catégories
	cats=set()
	
	with open(fichier) as f:
		for line in f:
			ligne=tabz.split(line.decode("utf-8"))
			
			#Si une troisième colonne est présente
			#Sa valeur est affectée à la variable _ qui ne sert pas
			if len(ligne) > 2:
				forme,cat,_=ligne
			else:
				forme,cat=ligne
			
			#Met en forme les noms de catégories tirés de lex.txt
			#Qui sont suivis d'un espace et d'une probabilité
			cat=re.sub(r" [0-9]\.[0-9]*","",cat,0,re.UNICODE)
			cat=cat.strip(" \"'\t\n").upper()
			
			if cat not in CLASSESFERMEES:
				#Mise en forme des valeurs récupérées :
				#Suppression des espaces
				if len(forme) > 1:
					forme=forme.strip("\"'\t\n")
				forme=re.sub(r"[ ]+","_",forme,0,re.UNICODE)
				
				#Suppression des blancs en fin de lignes 
				
			
			
				cats.add(cat)
			
				if c == TEST:
					test.append((forme,cat))
				else:
					train.append((forme,cat))
			
				c=random.randint(0,TEST)
			
			
	return test,train,cats

#Fonction énumérant toutes les sous-chaînes de la chaîne xs
def enumsubstrings(xs):
	subs=set()
	minlength=1
	for a in range(0,len(xs)-minlength):
		for b in range(a+minlength,len(xs)+1):
			subs.add(xs[a:b])
			subs.add(xs[a:b].lower())
	
	return subs			

#Fonction énumérant les suffixes de la chaîne xs
def enumsuffixe(xs):
	subs=set()
	for x in range(0,len(xs)):
		#subs[xs[x:]] = subs.get(xs[x:],0.0) + 1
		subs.add(xs[x:])
	return subs

#Fonction renvoyant un vecteur de traits pour une chaîne donnée
@memoize
def getfeatures(xs):
	traits=dict()
	traits['_biais_']=1.0
	
	if xs[0] in CAPITALES:
		traits['_capitale1_']=1.0
	if xs[-1] in CAPITALES:
		traits['_capitale-1_']=1.0
	if xs == xs.upper():
		traits['_ALLCAPS_']=1.0
	elif xs == xs.lower():
		traits['_downcase_']=1.0
	else:
		traits['_mIxEdCasE_']=1.0
	
	xs="#"+xs+"#"
	for e in enumsubstrings(xs):
		traits[e]=1.0
	
	return traits			

#Fonction renvoyant le score d'un vecteur de traits multiplié par un vecteur de poids
def score(w,traits):
	return sum([ w[t]*traits[t] for t in traits])

#Fonction de classification du perceptron
#Fait un argmax en conservant la deuxième meilleure étiquette pour la renvoyer aussi.
def classify(poids,traits):
	toto=poids.keys()
	defcat=random.choice(toto)
	a=(defcat,0.0)
	b=(defcat,0.0)
	for clef in toto:
		z=score(poids[clef],traits)
		if z > a[1]:
			b=a
			a=(clef,z)
		elif z > b[1]:
			b=(clef,z)
	
	return [a[0],b[0]]
	
	#return max(poids.keys(),key=lambda x : score(poids[x], traits))
	#return sorted(poids.keys(),key=lambda x: score(poids[x], traits),reverse=True)

#Fonction renvoyant un defaultdict ayant des floats pour valeur
#Utilisée pour créer le vecteur de poids car Pickle n'aime pas les lambdas
def defloat():
	return defaultdict(float) 

#Fonction d'entraînement du perceptron
#Entraîne un perceptron sur un corpus pour un nombre maximal d'itérations fixées à l'avance
#Le perceptron est par défaut moyenné
def perceptronmaker(cats,corpus,itermoi=10,averaged=True,shuffled=True,poids=defaultdict(defloat) ):

	for c in cats:
		poids[c]
	
	accum=defaultdict(lambda : defaultdict(float))
	i=0.0
	
	#Variable booléenne utilisée pour arrêter les itérations si le perceptron a 100% de bonnes réponses
	#(Ce qui n'arrive en pratique jamais)
	allright=False
	
	for iterations in range(0, itermoi):
		if allright:
			break
		
		allright=True
		
		if shuffled:
			random.shuffle(corpus)
		
		for (e,c) in corpus:
			truecat=c
			exemple=getfeatures(e)
			cat,zcat=classify(poids, exemple)[:2]
			if cat != truecat:
				allright=False
				for trait in exemple:
					poids[truecat][trait] = poids[truecat][trait] + exemple[trait]
					poids[cat][trait] = poids[cat][trait] - exemple[trait]
					
					#Accumulateur, utilisé pour le moyennage du perceptron 
					accum[truecat][trait] = accum[truecat][trait] + (exemple[trait]*i)
					accum[cat][trait] = accum[cat][trait] - (exemple[trait]*i)
				
			i+= 1
					
		print iterations+1
	
	print "Moyennage..."
	if averaged:
		for w in poids:
			for feat in poids[w]:
				poids[w][feat] = poids[w][feat] - (accum[w][feat]/(i+1))
	
	print "...fait"
			
	return poids


#Fonction pour sauver le vecteur de poids dans un fichier
#Prend un vecteur de poids en entrée, et optionnellement un nom de fichier.
#Les poids nuls sont éliminés pour ne pas alourdir le fichier.
def saveweights(weight,nom="weights.pickle"):
	m=weight.keys()
	for k in m:
		l=weight[k].keys()
		for z in l:
			if weight[k][z] == 0.0:
				del weight[k][z]
	
	with open(nom,'w') as toto:
		pickle.dump(weight,toto)
	
#Fonction pour charger un vecteur de poids à partir d'un fichier
def importpickle(filename):
	with open(filename) as toto:
		return pickle.load(toto)

#MUSIC HAS THE RIGHT TO CHILDREN

