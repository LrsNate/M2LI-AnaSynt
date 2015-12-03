#!/bin/sh

< in.txt 01_etiq_token_debruit/etape1.py \
| 02_morpho/etape2.py -p 02_morpho/weights.pickle -l 02_morpho/known.pickle \
| 03_spellcheck_compounds/group3.py \
| python 04_namedEntity/recognitionNE.py
