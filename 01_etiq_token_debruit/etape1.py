#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################
#				ANALYSE SYNTAXIQUE DU LANGAGE NATUREL				   #
#								  TP								   #
#																	   #
#								ÉTAPE 1								   #
#																	   #
#				Anaïs Chanclu			  Adrien Roux				   #
########################################################################

# Importations des bibliothèques
import codecs, re, sys

def lireCorpus(corpus):
	"""
	Lecture du corpus et écriture dans le fichier de sortie
	"""
	f = corpus.read()
	sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
		
	# Reconnaissance de la ponctuation forte		
	ponctForte = re.compile(u"([\.?!])\W")
	# Découpage en lignes
	lignes = ponctForte.sub(ur"\1\n", f)
	
	# Pour chaque ligne, on étiquette, on tokenise et on débruite
	for ligne in lignes.split(u"\n"):
		ligne = ponctuation(ligne)
		ligne = etiquettage(ligne)
		dico = tokenisation(ligne)
		dico = debruitage(dico)
					
		# On renvoie le résultat vers la sortie standard
		ponctForte = re.compile(u"([\.?!])\Z")
		for val in dico.values():
			if val[1] and val[2]:
				# Si le mot possède une étiquette :
				# original	étiquette
				sys.stdout.write(val[1] + "\t" + val[2] + "\n")
			elif val[1]:
				# Si le mot a été modifié :
				# original	modifié
				sys.stdout.write(val[1] + "\t" + val[0] + "\n")
			else:
				# Si le mot n'a pas été modifié et qu'il ne porte pas d'étiquette :
				#	original
				if ponctForte.search(val[0]):
					sys.stdout.write("\t" + val[0] + "\n\n")
				else:
				# On ajoute juste une ligne blanche après une ponctuation forte
					sys.stdout.write("\t" + val[0] + "\n")
			

def ponctuation(ligne):
	"""
	Traitement de la ponctuation
	"""
	# Ajout d'un saut à la ligne avant chaque ponctuation forte
	ponctForte = re.compile(u"([\.?!])\Z")
	ligne = ponctForte.sub(ur"\n\1\n", ligne)
	
	# Ajout d'un saut de ligne avant et après chaque ponctuation faible hors apostrophe
	ponctFaible = re.compile(u"([,;\(\)\[\]\{\}«»—])")
	ligne = ponctFaible.sub(ur"\n\1\n", ligne)
	
	# Ajout d'un saut de ligne après l'apostrophe
	apostrophe = re.compile(u"(['’])")
	ligne = apostrophe.sub(ur"\1\n", ligne)
	ligne = ligne.replace(u"aujourd(['’])\nhui", ur"aujourd\1hui")
	ligne = ligne.replace(u"presqu(['’])\nîle", ur"presque\1île")
	ligne = ligne.replace(u"ojourd(['’])\n8", ur"ojourd\18")
	ligne = ligne.replace(u"j(['’])\nle", ur"j\1le")
	ligne = ligne.replace(u"t(['’])\nm", ur"t\1m")
	ligne = ligne.replace(u"d(['’])\nacc", ur"d\1acc")
	ligne = ligne.replace(u"p(['’])\nti", ur"p\1ti")
	ligne = ligne.replace(u"p(['’])\ntit", ur"p\1tit")
	ligne = ligne.replace(u"v(['’])\nlà", ur"v\1là")
	ligne = ligne.replace(u"v(['’])\nla", ur"v\1la")
	ligne = ligne.replace(u"j(['’])\ntapldkej(['’])\npe", ur"j\1tapldkej\2pe")
	
	# Attention aux deux-points
	deuxpoints = re.compile(u"(\:)\s")
	ligne = deuxpoints.sub(ur"\n\1\n", ligne)
	
	return ligne

def etiquettage(ligne):
	"""
	Repérage et étiquettage des URL, emails, nombres, dates, heures, hastags, etc.
	"""
	# REVOIR TOUTES LES EXPRESSIONS REGULIERES !!!!!!!!!
	# Expressions régulières pour le repérage des étiquettes
	email = re.compile(ur"\b([\w\-_\.]+@[\w\-_\.]+\.[\w\-_\.]+)\b", re.I)
	url = re.compile(ur"(\s|\A)(((ht|f)tp(s)?://)?(www\.)?([\w\-\.]+)\.\w+([\w\-\./\?#]+)?\b)", re.I)
	hashtag = re.compile(u"\b(#\S+)")
	nombre = re.compile(u"(\s|\A)(\d+(\s\d{3})*(,\d+)?)(\s|\Z)")
	dateEU = re.compile(u"(\s|\A)(([12]\d|3[01]|0?[1-9])(([\.\-/])?(1[0-2]|0?[1-9])([\.\-/]?))(\d{0,4})?)(\s|\Z)")
	dateUS = re.compile(u"\b((\d{0,4})(([\.\-/])?(1[0-2]|0?[1-9])([\.\-/])?)([12]\d|3[01]|0?[1-9])?)\b")
	dateLettres = re.compile(u"(\b(((lun|mar|mercre|jeu|vendre|same)di\s+)|dimanche\s+)?((([12]\d)|(3[01])|(0?[2-9])|(1er))\s+)(janvier|février|mars|avril|mail|juin|juillet|août|(septem|octo|novem|décem)bre)(\s+\d{1,4})?\b)", re.I)
	heure = re.compile(ur"\b(((0?\d)|(1\d)|(2[0-3]))( *)(:|heure(s)?|h)( *)((0?\d)|([1-5]\d))?)\b", re.I)
	
	# Remplacer les espaces par un tilde pour ce qui se trouve entre {}
	reperage = re.compile(ur"(\{[^\}]+)\s+([^\{]+\})")
	
	# Application des expressions régulières et ajout du "commentaire" qui indique leur repérage
	if email.search(ligne):
		ligne = email.sub(ur"{\1}__EMAIL", ligne)
	if url.search(ligne):
		ligne = url.sub(ur"\1{\2}__URL", ligne)
	if dateLettres.search(ligne):
		ligne = dateLettres.sub(ur"{\2}__DATE", ligne)
	if heure.search(ligne):
		ligne = heure.sub(ur"{\1}__HEURE", ligne)
	#~ if dateEU.search(ligne):
		#~ ligne = dateEU.sub(ur"\1{\2}__DATE\9", ligne)
	if dateUS.search(ligne):		# On a-t-on vraiment besoin ?
		ligne = dateUS.sub(ur"{\1}__DATE", ligne)
	if hashtag.search(ligne):
		ligne = hashtag.sub(ur"{\1}__HASHTAG", ligne)
	if nombre.search(ligne):
		ligne = nombre.sub(ur"\1{\2}__NOMBRE\5", ligne)

	while reperage.search(ligne):
		ligne = reperage.sub(ur"\1~\2",ligne)

	return ligne

def tokenisation(ligne):
	"""
	Tokenisation des phrases en mots.
	ATTENTION : Les phrases sont seulement séparées en mots par les espaces.
	"""
	# Initialisation du dictionnaire et de l'indice
	dico = {}
	i = 1
	
	# Découpage en mots
	mots = ligne.split()
	
	# On crée un dictionnaire par phrase sous la forme suivante :
	# { 1 : [mot1, "", ""], 2 : [mot2, "motOrig", "etiqMot"], etc.}
	for mot in mots:
		if "{" in mot and "}" in mot:
			formOrig = re.compile(u"\{([^\}]+)\}")
			original = formOrig.sub(ur"\1", mot).split(u"__")[0]
			original = original.replace("~", " ")
			etiquette = mot.split(u"}_", 1)[1]
			dico[i] = [mot, original, etiquette]
			i+=1
		else:
			dico[i] = [mot, "", ""]
			i+=1
	
	return dico

def debruitage(dico):	
	"""
	Débruitage et correction des mots en langage SMS et abréviations
	"""
	# Dictionnaire de correspondance entre SMS et français	
	traduction = {
		u"ab1to" : u"à bientôt",
		u"ab" : u"à bientôt",
		u"akro" : u"accro",
		u"ht" : u"acheter",
		u"a2m1" : u"à demain",
		u"afr" : u"affaire",
		u"aj" : u"age",
		u"ajt" : u"agité",
		u"ajd" : u"aujourd'hui",
		u"ag" : u"âgé",
		u"asv" : u"âge sexe ville",
		u"éd" : u"aider",
		u"m" : u"aime",
		u"alp" : u"à la prochaine",
		u"alé" : u"aller",
		u"ar" : u"aller-retour",
		u"l1di" : u"lundi",
		u"ama" : u"à mon avis",
		u"apro" : u"apéro",
		u"a+" : u"à plus",
		u"@+" : u"à plus",
		u"aprè" : u"après",
		u"ap" : u"après",
		u"arét" : u"arrêter",
		u"ariv" : u"arriver",
		u"ok1" : u"aucun",
		u"oqne" : u"aucune",
		u"ojourd'8" : u"aujourd'hui",
		u"auj" : u"aujourd'hui",
		u"a12c4" : u"à un de ces quatre",
		u"oci" : u"aussi",
		u"avan" : u"avant",
		u"avanc " : u"avancer",
		u"balad" : u"balader",
		u"bavard" : u"bavarder",
		u"bcp" : u"beaucoup",
		u"bi1" : u"bien",
		u"b1" : u"bien",
		u"bi1sur" : u"bien sûr",
		u"b1sur" : u"bien sûr",
		u"bi1to" : u"bientôt",
		u"biz" : u"bises",
		u"bizz" : u"bises",
		u"bap" : u"bon après-midi",
		u"bjr" : u"bonjour",
		u"bj" : u"bonne journée",
		u"bn" : u"bonne nuit",
		u"bon8" : u"bonne nuit",
		u"bsr" : u"bonsoir",
		u"boc" : u"bosser",
		u"kdo" : u"cadeau",
		u"kdo" : u"cadeau",
		u"kfar" : u"cafard",
		u"ks" : u"caisse",
		u"kl1" : u"câlin",
		u"kfé" : u"café",
		u"knon" : u"canon",
		u"capou" : u"capoeira",
		u"kc" : u"casser",
		u"cv" : u"ça va",
		u"sava" : u"ça va",
		u"savapa" : u"ça va pas",
		u"ayé" : u"ça y est",
		u"cd" : u"céder",
		u"clibatr" : u"célibataire",
		u"cad" : u"c'est-à-dire",
		u"c-a-d" : u"c'est-à-dire",
		u"c-à-d" : u"c'est-à-dire",
		u"càd" : u"c'est-à-dire",
		u"cad" : u"c'est-à-dire",
		u"b1" : u"bien",
		u"ca" : u"ça",
		u"cho" : u"chaud",
		u"ckomen" : u"c'est comment",
		u"ct" : u"c'était",
		u"chang" : u"changer",
		u"reuch" : u"cher",
		u"chx" : u"cheveux",
		u"6gar" : u"cigare",
		u"6garett" : u"cigarette",
		u"6né" : u"ciné",
		u"6néma" : u"cinéma",
		u"klr" : u"clair",
		u"kler" : u"clair",
		u"koq" : u"cocu",
		u"ker" : u"coeur",
		u"colr" : u"colère",
		u"komand" : u"commander",
		u"kom" : u"comme",
		u"comen" : u"comment",
		u"koman" : u"comment",
		u"cmt" : u"comment",
		u"komencava" : u"comment ça va",
		u"koncr" : u"concert",
		u"co" : u"connecter",
		u"kontst" : u"contester",
		u"cok1" : u"coquin",
		u"cc" : u"coucou",
		u"croa" : u"crois",
		u"croiz" : u"croise",
		u"krul" : u"cruel",
		u"d'acc" : u"d'accord",
		u"dacc" : u"d'accord",
		u"dak" : u"d'accord",
		u"danc" : u"dancer",
		u"ds" : u"dans",
		u"dla" : u"de la",
		u"d6d" : u"décider",
		u"2labal" : u"de la balle",
		u"2labomb" : u"de la bombe",
		u"2m1" : u"demain",
		u"2mand" : u"demander",
		u"dpenc" : u"dépenser",
		u"drang" : u"déranger",
		u"dé" : u"des",
		u"asap" : u"dès que possible",
		u"d100" : u"descends",
		u"dsl" : u"désolé",
		u"dtst" : u"détester",
		u"2van" : u"devant",
		u"10ko" : u"dictionnaire",
		u"d1gue" : u"dingue",
		u"diskut" : u"discuter",
		u"10kut" : u"discuter",
		u"dc" : u"donc",
		u"dout" : u"douter",
		u"écout" : u"écouter",
		u"empr1t" : u"emprunter",
		u"nrv" : u"énervé",
		u"nrv" : u"énervé",
		u"véner" : u"énervé",
		u"enfr" : u"enfer",
		u"e.g." : u"par exemple",
		u"e.g" : u"par exemple",
		u"eg" : u"par exemple",
		u"k" : u"cas",
		u"épat" : u"épater",
		u"xpldr" : u"explosé de rire",
		u"xtrm " : u"extrême",
		u"fr" : u"faire",
		u"fb" : u"facebook",
		u"fo" : u"faut",
		u"fet" : u"fête",
		u"flip" : u"flipper",
		u"flem" : u"flemme",
		u"ouf" : u"fou",
		u"francè" : u"français",
		u"francé" : u"français",
		u"fr" : u"france",
		u"frr" : u"frère",
		u"fr8 " : u"fruit",
		u"gan" : u"gant",
		u"mek" : u"mec",
		u"ga" : u"gars",
		u"gnial" : u"génial",
		u"grav" : u"grave",
		u"gro" : u"gros",
		u"abit" : u"habiter",
		u"azar" : u"hasard",
		u"ézit" : u"hésiter",
		u"ere" : u"heureux",
		u"erez" : u"heureuse",
		u"i.e." : u"c'est-à-dire",
		u"i.e" : u"c'est-à-dire",
		u"ie" : u"c'est-à-dire",
		u"ir" : u"hier",
		u"ier" : u"hier",
		u"1bcile" : u"imbécile",
		u"1posibl" : u"impossible",
		u"1diféren" : u"indifférent",
		u"1fo" : u"info",
		u"1trec" : u"intéressé",
		u"g" : u"j'ai",
		u"gf1" : u"j'ai faim",
		u"jalou" : u"jaloux",
		u"jamé" : u"jamais",
		u"jms" : u"jamais",
		u"j'le" : u"je le",
		u"jle" : u"je le",
		u"sav" : u"savais",
		u"déco" : u"déconnecte",
		u"jenémar" : u"j'en ai marre",
		u"lol" : u"mort de rire",
		u"jspr" : u"j'espère",
		u"ktu" : u"que tu",
		u"chuis" : u"je suis",
		u"jtd" : u"je t'adore",
		u"jtdr" : u"je t'adore",
		u"jtm" : u"je t'aime",
		u"t'm" : u"t'aime",
		u"jtaime" : u"je t'aime",
		u"j'tapldkej'pe" : u"je t'appelle dès que je peux",
		u"jetelédjadi" : u"je te l'ai déjà dit",
		u"jtv" : u"je te vois",
		u"v" : u"vais",
		u"vé" : u"vais",
		u"jt" : u"journal télévisé",
		u"jr" : u"jour",
		u"jug" : u"juger",
		u"1mn" : u"une minute",
		u"jv" : u"j'y vais",
		u"karat" : u"karaté",
		u"lh" : u"lâche",
		u"lès" : u"laisse",
		u"lak" : u"laquelle",
		u"lekl" : u"lequel",
		u"li" : u"lit",
		u"l8" : u"lui",
		u"magaz1" : u"magasin",
		u"manifik" : u"magnifique",
		u"m1tnan" : u"maintenant",
		u"mnt" : u"maintenant",
		u"mé" : u"mais",
		u"mézon" : u"maison",
		u"méson" : u"maison",
		u"malad" : u"malade",
		u"mal1" : u"malin",
		u"mang" : u"manger",
		u"mh" : u"manque d'humour",
		u"manké" : u"manquer",
		u"mat1" : u"matin",
		u"mov" : u"mauvais",
		u"mové" : u"mauvais",
		u"max" : u"maximum",
		u"chanmé" : u"méchant",
		u"mm" : u"même",
		u"mrd" : u"merde",
		u"ménag" : u"ménager",
		u"m." : u"monsieur",
		u"m" : u"monsieur",
		u"mm" : u"madame",
		u"mme" : u"madame",
		u"msg" : u"message",
		u"trom" : u"métro",
		u"mn" : u"minute",
		u"min" : u"minute",
		u"jvb" : u"je vais bien",
		u"-" : u"moins",
		u"mdr" : u"mort de rire",
		u"moy1" : u"moyen",
		u"musq" : u"musculation",
		u"muzik" : u"musique",
		u"zik " : u"musique",
		u"nécsr" : u"nécessaire",
		u"nrve" : u"nerveux",
		u"nc" : u"no comment",
		u"nb" : u"nombre",
		u"nbr" : u"nombre",
		u"nbx" : u"nombreux",
		u"nouvl" : u"nouvelle",
		u"nouvo" : u"nouveau",
		u"nvx" : u"nouveaux",
		u"oqp" : u"occupé",
		u"remps" : u"parents",
		u"partou" : u"partout",
		u"partt" : u"partout",
		u"pa" : u"pas",
		u"pdp" : u"pas de problème",
		u"plpp" : u"pas libre pour parler",
		u"pac" : u"passer",
		u"péyé" : u"payer",
		u"pd" : u"pédé",
		u"konar" : u"connard",
		u"salop" : u"salope",
		u"kon" : u"kon",
		u"bg" : u"beau gosse",
		u"salo" : u"salaud",
		u"pdt" : u"pendant",
		u"ptdr" : u"pété de rire",
		u"pti" : u"petit",
		u"ptit" : u"petit",
		u"ptite" : u"petite",
		u"p'ti" : u"petit",
		u"p'tit" : u"petit",
		u"p'tite" : u"petite",
		u"pe" : u"peu",
		u"foto" : u"photo",
		u"pig" : u"piger",
		u"sniiif" : u"snif",
		u"sniif" : u"snif",
		u"sniiiif" : u"snif",
		u"+" : u"plus",
		u"poa" : u"poids",
		u"po1" : u"point",
		u"poz" : u"poser",
		u"pr" : u"pour",
		u"4me" : u"pour moi",
		u"pk" : u"pourquoi",
		u"prtan" : u"pourtant",
		u"prtant" : u"pourtant",
		u"4u" : u"pour toi",
		u"pb" : u"problème",
		u"prob" : u"problème",
		u"blèm" : u"problème",
		u"blème" : u"problème",
		u"qd" : u"quand",
		u"kan" : u"quand",
		u"ke" : u"que",
		u"kel" : u"quel",
		u"kelkun" : u"quelqu'un",
		u"qqun" : u"quelqu'un",
		u"keske" : u"qu'est-ce que",
		u"kestufé" : u"qu'est-ce que tu fais",
		u"kekiya" : u"qu'est-ce qu'il y a",
		u"kestion" : u"question",
		u"ki" : u"qui",
		u"kil" : u"qu'il",
		u"quit" : u"quitter",
		u"koi" : u"quoi",
		u"koa" : u"quoi",
		u"kwa" : u"quoi",
		u"kon" : u"qu'on",
		u"rapl" : u"rappel",
		u"rapv" : u"rappellez vite",
		u"ra" : u"ra",
		u"rat" : u"rater",
		u"regar2" : u"regarde",
		u"rejo1" : u"rejoins",
		u"rdv" : u"rendez-vous",
		u"rstp" : u"réponds s'il te plaît",
		u"rsvp" : u"répondez s'il vous plaît",
		u"rep" : u"réponse",
		u"re" : u"resalut",
		u"resto" : u"restaurant",
		u"réu" : u"réunion",
		u"réucir" : u"réussir",
		u"ri1" : u"rien",
		u"ras" : u"rien à signaler",
		u"ru" : u"rue",
		u"sal" : u"sale",
		u"slt" : u"salut",
		u"sem" : u"semaine",
		u"semn" : u"semaine",
		u"srai" : u"serais",
		u"stp" : u"s'il te plaît",
		u"stvcqjvd" : u"si tu vois ce que je veux dire",
		u"sk8" : u"skate",
		u"seur" : u"soeur",
		u"st" : u"sont",
		u"svt" : u"souvent",
		u"spor" : u"sport",
		u"svp" : u"s'il vous plaït",
		u"sdr" : u"suis de retour",
		u"5pa" : u"sympa",
		u"tg" : u"ta gueule",
		u"tm" : u"t'aime",
		u"tr" : u"taire",
		u"tps" : u"temps",
		u"t" : u"t'es",
		u"tt" : u"tout",
		u"tabitou" : u"tu habites où",
		u"thx" : u"thanks",
		u"tkt" : u"t'inquiète",
		u"2day" : u"today",
		u"twa" : u"toi",
		u"tjr" : u"toujours",
		u"tjrs" : u"toujours",
		u"tt" : u"tout",
		u"tr1" : u"train",
		u"trankil" : u"tranquille",
		u"tafé" : u"taffer",
		u"tro" : u"trop",
		u"vazi" : u"vas-y",
		u"vazy" : u"vas-y",
		u"vlo" : u"vélo",
		u"vnez" : u"venez",
		u"vr" : u"vers",
		u"vi1" : u"viens",
		u"vivmnt" : u"vivement",
		u"vla" : u"voilà",
		u"vlà" : u"voilà",
		u"v'là" : u"voilà",
		u"v'la" : u"voilà",
		u"vs" : u"vous",
		u"vou" : u"vous",
		u"voyag" : u"voyager",
		u"vrémen " : u"vraiment",
		u"we" : u"week-end",
		u"w-e " : u"week-end",
		u"yx" : u"yeux",
		u"zn" : u"zen",
		u"gg" : u"good game",
		u"fdp" : u"fils de pute",
		u"avé" : u"avez",
		u"r1" : u"rien",
		u"fair" : u"faire",
		u"d" : u"de",
		u"xd" : u"",
		u":d" : u"",
		u":-d" : u"",
		u":)" : u"",
		u":-)" : u"",
		u";)" : u"",
		u";-)" : u"",
		u";p" : u"",
		u";-p" : u"",
		u":3" : u"",
		u"^^" : u"",
		u"o" : u"au",
		u"c" : u"c'est",
		u"boulo" : u"boulot",
		u"é" : u"et",
		u"fau" : u"faut",
		u"fo" : u"faut",
		u"trouv" : u"trouv",
		u"komen" : u"comment",
		u"koman" : u"comment",
		u"mieu" : u"mieux",
		u"pasé" : u"passer",
		u"ken" : u"qu'en",
		u"tou" : u"tout",
		u"lé" : u"les",
		u"jusko" : u"jusqu'au",
		u"juskau" : u"jusqu'au",
		u"jv" : u"j'y vais",
	}
	
	# Remplissage du dictionnaire suivant le dictionnaire de correspondance
	for val in dico.values():
		if val[0].lower() in traduction.keys():
			val[1] = val[0]
			val[0] = traduction[val[0].lower()]
			
	# Retokenisation pour les mots qui possèdent un espace
	i = 1
	for cle, val in dico.items():
		# Si un mot possède un espace et que sa forme originale se trouve dans le dictionnaire de traduction
		if " " in val[0] and val[1] in traduction:
			listeMots = val[0].split()
			lenListeMots = len(listeMots)
			j = 1
			while j <= lenListeMots:
				dico[i] = [listeMots[0], val[1], val[2]]
				listeMots.remove(listeMots[0])
				i += 1
				j += 1
		else:
			dico[i] = dico[cle]
			i += 1

	return dico

# Stockage de l'entrée dans une variable.
corpus = codecs.getreader("utf-8")(sys.stdin)

lireCorpus(corpus)
