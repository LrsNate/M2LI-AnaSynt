# M2 LI Syntactic Analysis Project

Le script `run.sh` a maintenant un mode debug qui sort les outputs de chaque étape dans un fichier séparé.

Exécuter `./run.sh -d` sortira les fichiers `out_01.txt`, `out_02.txt`, `out_03.txt` et `out_04.txt`.

## OUTPUT GROUPE 1
`{ORIG_ORTH;}_CORR_ORTH`

Notes :
- Il y a une phrase par ligne. Les phrases sont découpées selon les ponctuations fortes.
- Dans `CORR_ORTH` on retrouve aussi bien les mots corrigés que les étiquettes.
- S'il n'y a pas de point final, il y aura une espace après le dernier mot de la dernière ligne.

Exemples :
```
{ORIG_ORTH='c';}c' {ORIG_ORTH='c';}est {ORIG_ORTH='ke';}que {ORIG_ORTH='c';}c' {ORIG_ORTH='c';}est rigolo a {ORIG_ORTH='fair';}faire {ORIG_ORTH='jv';}j' {ORIG_ORTH='jv';}y {ORIG_ORTH='jv';}vais .
Pi égale {ORIG_ORTH='3,14';}_NOMBRE
```

	=> Le groupe 5 a une requête... Vous identifiez les étiquettes avec des regex, non ? Si oui, est-ce que vous pourriez fournir un .txt avec colonne1_regex "\t" colonne2_étiquette (pour faire les substitutions dans le trainset) ? Ca serait génial ! Merci...
> Est-ce que le fichier `01_etiq_token_debruit/regex_etiquettes.txt` convient ?
OUI :) (439 remplacements sur mon TRAINCORP)

Le groupe 3 (enfin, un des binomes) a une petite remarque de formatage : c'est pas plus cohérent de suivre l'input/output du prof sur toute la chaîne ? En l'occurrence une phrase par ligne et chaque token formaté en `{annotations}forme`. En l'occurrence ça pourrait ressembler à quelque chose comme `{SMS='koi'}quoi` ou `{NE_NAME='toto@github.com'}_EMAIL`. Tu en penses quoi ?
> C'est fait.

## OUTPUT GROUPE 2

Les mots étiquetés prendrons typiquement cette forme : `{TMP_TAG='TAG1,TAG2';}word`
Si un mot étiqueté était déjà précédé par des accolades, `TMP_TAG='TAG1,TAG2';` sera concaténé au contenu de ces accolades, sans espace. On part du principe que ce contenu se finit déjà par un point-virgule. 

## OUTPUT GROUPE 3

Note : s'il y a plusieurs attributs, ils seront separes par un point-virgule (`;`).

`{ORIG_ORTH=token_with_error}corrected_token`

`EX: {ORIG_ORTH='chein'}chien`

`{ORIG_SEG=[token,token];ORIG_ATTR_N='...';...}compound_word`

```
EX: {TAG='N'}pomme {TAG='P'}de {TAG='N'}terre
-> {ORIG_SEG=['pomme','de','terre'];TAG_1='N';TAG_2='P';TAG_3='N'}pomme_de_terre__N
```

`{AML='original_token'}split_token {AML='original_token'}split_token`

`Ex: {AML='du'}de {AML='du'}le`

Exemple complet:

```
echo "{TAG='A'}bien {TAG='A'}sûr duquel {TMP_TAG='a'}entropie visuellemnt {TMP_TAG='xsa'}carbonne {TMP_TAG='N'}quztre cinq" | ./group3.py
{TAG_0='A';TAG_1='A';ORIG_SEG=['bien','sûr']}bien_sûr {AML='duquel'}de {AML='duquel'}lequel {ORIG_ORTH='entropie';TMP_TAG='a'}entrions visuellemnt {ORIG_ORTH='carbonne';TMP_TAG='xsa'}carbone {ORIG_ORTH='quztre';TMP_TAG='N'}quatre cinq
```

## OUTPUT GROUPE 4
in: `en provenance d' un {ORIG_ORTH='fjord';TMP_TAG='NC,ADJ'}flore {AML='du'}de {AML='du'}le {TMP_TAG='NPP,ET'}Groenland .`

out: `en provenance d' un {ORIG_ORTH='fjord';TMP_TAG='NC,ADJ'}flore {AML='du'}de {AML='du'}le {TMP_TAG='NPP,ET';ORIG='Groenland';LIEN='https://fr.wikipedia.org/wiki/Groenland'}_LOC . `

## OUTPUT GROUPE 5
Alors, si j'ai bien tout compris (oui, je sais, avec des si pareils, on mettrait Paris en bouteille...). Je dois envoyer au parser un truc de ce format là :
	Le _unknown_N part de le principe que _PERS_ est à le _PLACE_ . 
Tout en gardant en mémoire :
	Le shtroumpf paart du principe que Chomsky esst au Paradis.
