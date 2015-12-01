# M2 LI Syntactic Analysis Project

## OUTPUT GROUPE 1
`ORIG_ORTH      CORR_ORTH`

Notes :
- Il y a une ligne vide entre chaque phrase.
- Si un mot n'a pas été corrigé, il se trouve dans la colonne de droite.
- Les étiquettes se trouvent dans la colonne de droite.

Exemples :
```
slt    salut
        il
        est
11h30   _HEURE
        .

        tu
fais    fé
quoi    koi
        ?
```

	=> Le groupe 5 a une requête... Vous identifiez les étiquettes avec des regex, non ? Si oui, est-ce que vous pourriez fournir un .txt avec colonne1_regex "\t" colonne2_étiquette (pour faire les substitutions dans le trainset) ? Ca serait génial ! Merci...

Est-ce que le fichier `01_etiq_token_debruit/regexetiquettes.txt` convient ?

Le groupe 3 (enfin, un des binomes) a une petite remarque de formatage : c'est pas plus cohérent de suivre l'input/output du prof sur toute la chaîne ? En l'occurrence une phrase par ligne et chaque token formaté en `{annotations}forme`. En l'occurrence ça pourrait ressembler à quelque chose comme `{SMS='koi'}quoi` ou `{NE_NAME='toto@github.com'}_EMAIL`. Tu en penses quoi ?

## OUTPUT GROUPE 2

`{TMP_TAG='N,V'}word`

## OUTPUT GROUPE 3

Note : s'il y a plusieurs attributs, ils seront separes par un point-virgule (`;`).

`{ORIG_ORTH=token_with_error}corrected_token`

`EX: {ORIG_ORTH="chein"}chien`

`{ORIG_SEG=[token,token];ORIG_ATTR_N='...';...}compound_word`

```
EX: {TAG='N'}pomme {TAG='P'}de {TAG='N'}terre
-> {ORIG_SEG=["pomme","de","terre"];TAG_1='N';TAG_2='P';TAG_3='N'}pomme_de_terre__N
```

`{AML="original_token"}split_token {AML="original_token"}split_token`

`Ex: {AML="du"}de {AML="du"}le`

Exemple complet:

```
echo "{TAG='A'}bien {TAG='A'}sûr duquel {TMP_TAG='a'}entropie visuellemnt {TMP_TAG='xsa'}carbonne {TMP_TAG='N'}quztre cinq" | ./group3.py
{TAG_0='A';TAG_1='A';ORIG_SEG=["bien","sûr"]}bien_sûr {AML="duquel"}de {AML="duquel"}lequel {ORIG_ORTH="entropie";TMP_TAG='a'}entrions visuellemnt {ORIG_ORTH="carbonne";TMP_TAG='xsa'}carbone {ORIG_ORTH="quztre";TMP_TAG='N'}quatre cinq
```

## OUTPUT GROUPE 4

## OUTPUT GROUPE 5
