#!/usr/bin/env python3


class Automaton:
    """ A generic finite-state machine """
    def __init__(self):
        self.transitions = {}
        self.end_states = {}
        self.last_state = 1

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
    a = Automaton()
    _path = 'resources/lexique_cmpnd_utf8.txt'
    _file = open(_path, 'r')

    for line in _file:
        line = line.strip()
        rule = line.split('\t')
        a.learn_rule(rule[0].split(' '), (rule[0], rule[1], rule[2]))

    _file.close()
    return a

compounds_automaton = _make_compounds_automaton()

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

    class CompoundsAutomatonTest(unittest.TestCase):
        def test_recognition(self):
            res = compounds_automaton.recognize(['en', 'raison', 'du'])
            self.assertEqual(res, ('en raison du', 'P', 'en raison de+le'))

    unittest.main()