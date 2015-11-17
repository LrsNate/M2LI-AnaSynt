#!/usr/bin/env python
# -*- encoding:utf8 -*-

from utils import closest_word, expand_amalgam
from automaton import compounds_automaton
import fileinput
import pickle

wico = pickle.load(open('resources/results_wico.p', 'r'))

# TODO: Implement annotations (split words into annotations and form)
for line in fileinput.input():
    line = line.strip()
    words = line.split(' ')
    spellchecked = []
    # Step 1: spellcheck
    for w in words:
        # Detect if word is unknown
        if w in wico:
            spellchecked.append('{ORIG_ORTH="%s"}%s' % (w, wico[w]))
        else:
            lefff = []  # Haha. I know.
            lefff_corr = closest_word(lefff, w)
            if lefff_corr:
                spellchecked.append('{ORIG_ORTH="%s"}%s' % (w, lefff_corr))
            else:
                spellchecked.append(w)

    # Step 2: compound words
    merged = []
    slen = len(spellchecked)
    i = 0
    while i < len(spellchecked):
        res = compounds_automaton.recognize(spellchecked[i:])
        if res:
            comp, clist, tag, clen = res
            merged.append('{ORIG_SEG=[%s]}%s__%s' % (','.join(clist), comp, tag))
            i += clen
        else:
            merged.append(spellchecked[i])
            i += 1

    # Step 3: amalgams
    expanded = []
    for w in merged:
        am = expand_amalgam(w)
        if len(am) > 1:
            am = map(lambda x: '{AML="%s"}%s' % (w, x), am)
        expanded.extend(am)

    print(' '.join(expanded))
