#!/usr/bin/env python3
# -*- encoding:utf8 -*-
# @author : JTanon

import sys
import xml.etree.ElementTree as etree
import pickle
from collections import defaultdict

try:
    wico_file = sys.argv[1]
except:
    sys.exit("File missing")

lefff_file = open("lefff_5000.ftb4tags", "r")
lefff = []
line = lefff_file.readline()
while line:
    if line != "":
        try:
            form, _, _ = line.split()
        except:
            form = ' '.join(line.split()[:-2])
        lefff.append(form)
    line = lefff_file.readline()

print "lefff done..."

for i in range(1, 18):
    print "wico_"+str(i)+".xml"
    fic = open("wico_"+str(i)+".xml", "r")
    tree = etree.parse(wico_file)
    root = tree.getroot()
    results = defaultdict(str)
    mod_tot = 0
    for modif in root.iter('modif'):
        mod_tot += 1
        before = modif.find('before').find('m')
        after = modif.find('after').find('m')
        error = before.text
        correction = after.text
        nb_before = before.get('num_words')
        nb_after = after.get('num_words')
        if nb_before == "1":
            if nb_after == "1":
                if error in lefff:
                    pass
                else:
                    results[error] = correction
            elif nb_after == "2":
                space = set(error)
                space.add(' ')
                if space == set(correction):
                    results[error] = correction
            else:
                pass

pickle.dump(results, open("results_wico.p", "w"))
