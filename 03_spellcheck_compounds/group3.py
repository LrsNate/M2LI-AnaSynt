#!/usr/bin/env python
# -*- encoding:utf8 -*-

from utils import *
from automaton import compounds_automaton
import fileinput
import pickle

wico = pickle.load(open('resources/results_wico.p', 'r'))
lefff = pickle.load(open('lefff_pickle.p', 'r'))
# TODO: Implement annotations (split words into annotations and form)
for line in fileinput.input():
    line = line.strip()
    words = map(Token.from_str, line.split(' '))
    spellchecked = []
    # Step 1: spellcheck
    for w in words:
        # Detect if word is unknown
        if w.getform() in wico:
            spellchecked.append(Token.update_spelling(w, wico[w.getform()]))
        else:
            #lefff = []  # Haha. I know.
            lefff_cand = get_candidates_from_lefff(w.getform())
            lefff_corr = closest_word(lefff_cand, w.getform())
            if lefff_corr:
                spellchecked.append(Token.update_spelling(w, lefff_corr))
            else:
                spellchecked.append(w)

    # Step 2: compound words
    merged = []
    slen = len(spellchecked)
    i = 0
    while i < len(spellchecked):
        # TODO include annotations in merge
        res = compounds_automaton.recognize(map(lambda x: x.getform(), spellchecked[i:]))
        if res:
            comp, clist, tag, clen = res
            merged.append(Token.merge(clist, comp))
            i += clen
        else:
            merged.append(spellchecked[i])
            i += 1

    # Step 3: amalgams
    expanded = []
    for w in merged:
        am = expand_amalgam(w.getform())
        if len(am) > 1:
            expanded.extend(Token.expand(w, am))
        else:
            expanded.append(w)

    print(' '.join(map(lambda x: str(x), expanded)))
