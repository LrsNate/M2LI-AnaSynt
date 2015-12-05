#!/usr/bin/env python
# -*- coding:utf8 -*-

from utils import Token, get_candidates_from_lefff
from utils import closest_word, expand_amalgam
import os
from automaton import compounds_automaton, lexicon_automaton
import fileinput
import pickle
import re

dir = os.path.dirname(__file__)
wico = pickle.load(open(os.path.join(dir, 'resources/results_wico.p'), 'r'))


for line in fileinput.input():
    line = line.strip().decode('utf-8')
    line = re.sub(r'(\d) (\d)', r'\1_\2', line)
    words = map(Token.from_str, line.split(' '))
    spellchecked = []
    # Step 1: spellcheck
    for w in words:
        if u'TMP_TAG' not in w.getannotations() or \
           lexicon_automaton.recognize(list(w.getform())) or \
           w.getform()[0] == w.getform()[0].upper():
            spellchecked.append(w)
            continue
        if w.getform() in wico:
            wico_w = unicode(wico[w.getform()])
            spellchecked.append(Token.update_spelling(w, wico_w))
        else:
            lefff_cand = get_candidates_from_lefff(w.getform())
            lefff_corr = closest_word(lefff_cand, w.getform())
            if lefff_corr and lefff_corr != w.getform():
                spellchecked.append(Token.update_spelling(w, lefff_corr))
            else:
                spellchecked.append(w)

    # Step 2: compound words
    merged = []
    slen = len(spellchecked)
    i = 0
    while i < len(spellchecked):
        # TODO include annotations in merge
        res = compounds_automaton.recognize(
            map(lambda x: x.getform(), spellchecked[i:]))
        if res:
            comp, clist, tag, clen = res
            merged.append(Token.merge(spellchecked[i:i + clen], comp))
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

    print(' '.join(map(lambda x: unicode(x), expanded)).encode('utf-8'))
