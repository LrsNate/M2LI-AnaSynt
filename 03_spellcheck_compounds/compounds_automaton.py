#!/usr/bin/env python3

from automaton import Automaton

_path = 'resources/lexique_cmpnd_utf8.txt'
_file = open(_path, 'r')

compounds_automaton = Automaton()
for line in _file:
    line = line.strip()
    rule = line.split('\t')
    compounds_automaton.learn_rule(rule[0].split(' '), (rule[0], rule[1], rule[2]))

_file.close()

if __name__ == '__main__':
    import unittest

    class CompoundsAutomatonTest(unittest.TestCase):
        def test_recognition(self):
            res = compounds_automaton.recognize(['en', 'raison', 'du'])
            self.assertEqual(res, ('en raison du', 'P', 'en raison de+le'))

    unittest.main()
