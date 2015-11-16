#!/usr/bin/env python
# -*- encoding:utf8 -*-

from automaton import compounds_automaton
import fileinput
import pickle

wico = pickle.load(open('ressources/results_wico.p', 'r'))

for line in fileinput.input():
    line = line.strip()
    words = line.split(' ')
    result = []
    for w in words:
        # Detect if word is unknown
        if w in wico:
            result.append('{ORIG_ORTH="%s"}%s' % (w, wico[w]))
        # Run levenshtein on LeFFF (loaded from where?)
        else:
            result.append(w)
    print(' '.join(result))
