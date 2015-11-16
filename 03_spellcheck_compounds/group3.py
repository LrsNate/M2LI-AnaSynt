#!/usr/bin/env python
# -*- encoding:utf8 -*-

from utils import closest_word
from automaton import compounds_automaton
import fileinput
import pickle

wico = pickle.load(open('resources/results_wico.p', 'r'))

for line in fileinput.input():
    line = line.strip()
    words = line.split(' ')
    spellchecked = []
    # Step 1: spellcheck
    for i in range(len(words)):
        # Detect if word is unknown
        if words[i] in wico:
            spellchecked.append('{ORIG_ORTH="%s"}%s' % (words[i], wico[words[i]]))
        else:
            lefff = []  # Haha. I know.
            lefff_corr = closest_word(lefff, words[i])
            if lefff_corr:
                spellchecked.append('{ORIG_ORTH="%s"}%s' % (words[i], lefff_corr))
            else:
                spellchecked.append(words[i])

    # Step 2: compound words
    merged = []
    slen = len(spellchecked)
    i = 0
    while i < len(spellchecked):
        res = compounds_automaton.recognize(words[i:])
        if res:
            comp, clist, tag, clen = res
            merged.append('{ORIG_SEG=[%s]}%s__%s' % (','.join(clist), comp, tag))
            i += clen
        else:
            merged.append(spellchecked[i])
            i += 1

    print(' '.join(merged))
