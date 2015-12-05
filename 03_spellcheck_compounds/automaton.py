#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle


class Automaton:
    """ A generic finite-state machine """
    def __init__(self, bounded=True):
        self.transitions = {}
        self.end_states = {}
        self.last_state = 1
        self.bounded = bounded

    def learn_rule(self, tokens, rule):
        """
        Makes the automaton learn a new rule.
        :param tokens: A list of tokens describing the rule.
        :param rule: The rule itself. It will be returned by
            the recognition method.
        """
        curr_st = 0  # current_state
        for w in tokens:
            if curr_st not in self.transitions:
                self.transitions[curr_st] = {w: self.last_state}
                self.last_state += 1
            elif w not in self.transitions[curr_st]:
                self.transitions[curr_st][w] = self.last_state
                self.last_state += 1
            curr_st = self.transitions[curr_st][w]

        self.end_states[curr_st] = rule

    def recognize(self, tokens):
        """
        Tries to recognize a word from a set of rules.
        :param tokens: A list of tokens to be recognized.
        :return: The resulting rule in the automaton's grammar, or None.
        """
        curr_st = 0  # current_state
        for w in tokens:
            if not self.bounded and curr_st in self.end_states:
                return self.end_states[curr_st]
            if (curr_st not in self.transitions or
                    w not in self.transitions[curr_st]):
                return None
            curr_st = self.transitions[curr_st][w]
        if curr_st not in self.end_states:
            return None

        return self.end_states[curr_st]


def _make_compounds_automaton():
    """
    Trains an automaton to recognize compound words.
    :return: The trained automaton.
    """
    a = Automaton(bounded=False)
    _dir = os.path.dirname(__file__)
    _path = os.path.join(_dir, 'resources/lexique_cmpnd_utf8.txt')
    _file = open(_path, 'r')

    for line in _file:
        line = line.strip()
        rule = line.split('\t')
        words = rule[0].split(' ')
        a.learn_rule(words, ('_'.join(words), words, rule[1], len(words)))

    _file.close()
    return a

_dir = os.path.dirname(__file__)
compounds_automaton = cPickle.load(open(os.path.join(_dir, 'resources/compounds_automaton.p'), 'r'))
lexicon_automaton = cPickle.load(open(os.path.join(_dir, 'resources/lexicon_automaton.p'), 'r'))

if __name__ == '__main__':
    import unittest

    class AutomatonTest(unittest.TestCase):
        def test_emptylanguage(self):
            a = Automaton()
            self.assertIsNone(a.recognize([]))
            self.assertIsNone(a.recognize(['some_token']))

        def test_training(self):
            a = Automaton()
            a.learn_rule(['a', 'a', 'b'], 'r1')
            a.learn_rule(['a', 'b'], 'r2')
            self.assertEqual(a.recognize(['a', 'a', 'b']), 'r1')
            self.assertEqual(a.recognize(['a', 'b']), 'r2')

        def test_unbounded(self):
            a = Automaton(bounded=False)
            a.learn_rule(['a', 'a', 'b'], 'r1')
            a.learn_rule(['a', 'b'], 'r2')
            self.assertEqual(a.recognize(['a', 'a', 'b', 'b']), 'r1')
            self.assertEqual(a.recognize(['a', 'b', 'a']), 'r2')

    class CompoundsAutomatonTest(unittest.TestCase):
        def test_recognition(self):
            res = compounds_automaton.recognize(['en', 'raison', 'du'])
            self.assertEqual(res,
                             ('en_raison_du', ['en', 'raison', 'du'], 'P', 3))

    unittest.main()
