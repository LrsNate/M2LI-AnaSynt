#!/bin/sh

if [ "$1" =  "-d" ];
then
    01_etiq_token_debruit/etape1.py < in.txt > out_01.txt
    02_morpho/etape2.py -p 02_morpho/weights.pickle -l 02_morpho/known.pickle < out_01.txt > out_02.txt
    03_spellcheck_compounds/group3.py < out_02.txt > out_03.txt
    python 04_namedEntity/recognitionNE.py < out_03.txt > out_04.txt

    cat out_04.txt
else
    < in.txt 01_etiq_token_debruit/etape1.py \
    | 02_morpho/etape2.py -p 02_morpho/weights.pickle -l 02_morpho/known.pickle \
    | 03_spellcheck_compounds/group3.py \
    | python 04_namedEntity/recognitionNE.py
fi
