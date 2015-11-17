# M2 LI Syntactic Analysis Project

## OUTPUT GROUPE 1
Nous renvoyons à la condition de recevoir quarante millions d'euros de la part du groupe 2 un fichier texte composé de deux colonnes séparées par une tabulation :

La première colonne contient le mot original lorsque celui-ci a subi une modification.
La seconde colonne contient le mot original, le mot corrigé ou l'étiquette lorsque le mot a été modifié.

Exemples :
slt	salut
	il
	sait
	que
	ça
	ne
	va
	pas
	le
	faire
machin@bidule.truc	_EMAIL
11h30	_HEURE

Si vous avez des questions, veuillez prendre rendez-vous auprès de notre secrétaire (le prof, quoi).

## OUTPUT GROUPE 2

## OUTPUT GROUPE 3
`{ORIG_ORTH=token_with_error}corrected_token`

`EX: {ORIG_ORTH="chein"}chien`

`{ORIG_SEG=[(token,{_}),(token, {_})]}compound_word`

`EX: {ORIG_SEG=[("pomme",{}),("de",{}),("terre",{})]}pomme_de_terre__N`

`{AML="original_token"}split_token {AML="original_token"}split_token`

`Ex: {AML="du"}de {AML="du"}le`

## OUTPUT GROUPE 4

## OUTPUT GROUPE 5
