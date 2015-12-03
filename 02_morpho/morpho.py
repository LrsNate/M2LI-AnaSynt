#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import random
from functools import partial
from collections import defaultdict
import cPickle as pickle
import sys
from optparse import OptionParser

if __name__ == "__main__":
	usage=""
	p = OptionParser(usage=usage)
	p.add_option("-i","--iteration", action="store",dest="iteration", default=8,
	help=u"Nombres d'itérations du perceptron. Par défaut 8")

	p.add_option("-c", "--confusion",
		              action="store_true", dest="matrice", default=False,
		              help=u"Afficher les matrices de confusion")
	
	p.add_option("-t","--test", action="store_true",dest="testit", default=False,
	help=u"Option pour créer un corpus de test séparé pour tester le perceptron")


	(op,args)=p.parse_args()
	#Variables globales

	ITER=int(op.iteration)
	MATRICE=op.matrice
	TESTIT=op.testit
	TEST=9
	LATEX=False
	PERCENT=True

CAPITALES=u'ABCDEFGHIJKLMNOPQRSTUVWXYZÉÈÇÀÔÖÎÂÏÛÊË'
CLASSESFERMEES= []
#[u'P+D',u'P+PRO',u'ADJWH',u'ADVWH',u'CC',u'CLO',u'CLR',u'CLS',u'CS',u'DET',u'DETWH',u'P',u'PRO',u'PROREL',u'PROWH'] 

#Décorateur pour la mise en cache dans un dictionnaire de résultats de l'appel à une fonction
#Permet de limiter les appels à des fonctions couteuses en temps de calcul
#Cette technique de mémoisation est assez rudimentaire, elle ne fonctionne que pour les fonctions d'un seul argument
#En outre, l'argument de la fonction ne doit pas appartenir à un type mutable
def memoize(f):
	memo = {}
	def helper(x):
		if x not in memo:			
			memo[x] = f(x)
		return memo[x]
	return helper


#Fonction de lecture de corpus : prend un nom de fichier contenant des exemples
#Renvoie deux listes, train et test, de tuples (forme, catégorie), plus la liste des catégories relevées dans le fichier
def readlexicon(fichier):
	
	#Compiler les regexp octroie un léger gain de temps
	tabz=re.compile(r"\t")
	
	train,test=list(),list()
	
	c=random.randint(0,TEST)
	
	cats=set()
	
	with open(fichier) as f:
		for line in f:
			ligne=tabz.split(line.decode("utf-8"))
			
			if len(ligne) > 2:
				forme,cat,_=ligne
			else:
				forme,cat=ligne
			
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
			
				#c est une variable aléatoire comprise entre 0 et TEST
				#Pour chaque mot, si c est égal à la valeur TEST
				#La paire (forme,cat) est ajoutée dans le corpus de test
				#Sinon elle rejoint le corpus d'entraînement
				if c == TEST:
					test.append((forme,cat))
				else:
					train.append((forme,cat))
			
				c=random.randint(0,TEST)
			
			
	return test,train,cats

#Fonction énumérant toutes les sous-chaînes de la chaîne xs
def enumsubstrings(xs):
	#subs=list()
	subs=set()
	#subs=dict()
	minlength=1
	for a in range(0,len(xs)-minlength):
		for b in range(a+minlength,len(xs)+1):
			#subs.append(xs[a:b])
			subs.add(xs[a:b])
			subs.add(xs[a:b].lower())
			#subs[xs[a:b]] = subs.get(xs[a:b],0.0) + 1
	
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
		traits['_mixed_']=1.0
	
	
	#if "-" in xs:
	#	traits['_tiret_']=1
	#if "_" in xs:
	#	traits['_underscore_']=1
	#traits['_LEN_']=float(len(xs))
	
	xs="#"+xs+"#"
	for e in enumsubstrings(xs):
		traits[e]=1.0
	
	return traits			

#Fonction renvoyant le score d'un vecteur de traits multiplié par un vecteur de poids
def score(w,traits):
	return sum([ w[t]*traits[t] for t in traits])

#Fonction de classification du perceptron
import random 
def classify(poids,traits):
	toto=poids.keys()
	#a=max(toto,key=lambda x: score(poids[x], traits))
	#toto.remove(a)
	#b=max(toto,key=lambda x: score(poids[x], traits))
	a=(random.choice(toto),0.0)
	b=(random.choice(toto),0.0)
	for clef in toto:
		z=score(poids[clef],traits)
		if z > a[1]:
			b=a
			a=(clef,z)
		elif z > b[1]:
			b=(clef,z)
		
	#if a[1] == 0.0:
	#	print traits
	
	return [a[0],b[0]]
	
	#return sorted(poids.keys(),key=lambda x: score(poids[x], traits),reverse=True)

#Fonction renvoyant un defaultdict ayant des floats pour valeur
#Utilisée pour créer le vecteur de poids car Pickle n'aime pas les lambdas
def defloat():
	return defaultdict(float) 

#Fonction d'entraînement du perceptron
#Entraîne un perceptron sur un corpus pour un nombre maximal d'itérations fixées à l'avance
def perceptronmaker(cats,corpus,itermoi=10,averaged=True,shuffled=True,poids=defaultdict(defloat) ):
	
	for c in cats:
		poids[c]
	
	accum=defaultdict(lambda : defaultdict(float))
	i=0.0
	
	#corpuskeys=corpus.keys()
	
	#Variable booléenne utilisée pour arrêter les itérations si le perceptron a 100% de bonnes réponses
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
			#if cat != truecat:
			if truecat not in [cat,zcat]:
				allright=False
				for trait in exemple:
					poids[truecat][trait] = poids[truecat][trait] + exemple[trait]
					poids[cat][trait] = poids[cat][trait] - exemple[trait]
					
					#poids[zcat][trait] = poids[zcat][trait] - exemple[trait]
					
					#Accumulateur, utilisé pour le moyennage du perceptron 
					accum[truecat][trait] = accum[truecat][trait] + (exemple[trait]*i)
					accum[cat][trait] = accum[cat][trait] - (exemple[trait]*i)
					
					#accum[zcat][trait] = accum[zcat][trait] - (exemple[trait]*i)
				
			i+= 1
					
		print iterations+1
		#testit(test,partial(classify,poids),matrice=False)
	
	print "Moyennage..."
	if averaged:
		for w in poids:
			for feat in poids[w]:
				poids[w][feat] = poids[w][feat] - (accum[w][feat]/(i+1))
	
	print "...fait"
			
	return poids

#Fonction pour tester un classifieur
def testit(test,perceptron,matrice=True):
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
		#matcon[truecat,z] += 1
			
		#Nice = total des éléments bien catégorisés
		if y == truecat:
		#if truecat in [y,z]:
			nice += 1.0
		#elif z == truecat:
		#	nice += 0.5
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
		
#Fonction pour sauver le vecteur de poids dans un fichier
def saveweights(weight):
	m=weight.keys()
	for k in m:
		l=weight[k].keys()
		for z in l:
			if weight[k][z] == 0.0:
				del weight[k][z]
	
	with open("weights.pickle",'w') as toto:
		pickle.dump(weight,toto)

	
#Fonction pour charger un vecteur de poids à partir d'un fichier
def importweights(filename):
	with open(filename) as toto:
		return pickle.load(toto)

#-------------------------------------------------------------------------------------------------
#Programme
#Appeler avec les arguments : "../../TP Parsing M2LI/lefff_5000.ftb4tags" "../05_pcfg/lexicon2.txt" "../../TP Parsing M2LI/lexique_cmpnd_TP_unicode.txt"
#"../../TP Parsing M2LI/lefff_5000.ftb4tags"
#"../05_pcfg/lexicon2.txt"
#"../../TP Parsing M2LI/lexique_cmpnd_TP_unicode.txt"

if __name__ == "__main__":
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
	print "Entraînement du perceptron :"
	weight=perceptronmaker(cats,train,itermoi=ITER)

	perceptron=partial(classify,weight)

	#precision=0.0
	#for e in test:
	#	if perceptron(getfeatures(e)) == test[e]:
	#		precision += 1
	#precision= (100*precision/len(test))
	#print precision,"%"

	testit(test,perceptron,matrice=MATRICE)

	#raw_input()
	#meilleurstraits(weight)
	saveweights(weight)

	#while True:
	#	print perceptron(getfeatures(raw_input()))

