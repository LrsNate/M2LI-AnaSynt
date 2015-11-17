#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re


class Token:
    def __init__(self, annot, form):
        self.annot = annot
        self.form = form

    def getannotations(self):
        return self.annot

    def getform(self):
        return self.form

    def __str__(self):
        if not self.annot:
            return self.form
        res = '{'
        annot = map(lambda (k, v): '%s=%s' % (k, v), self.annot.iteritems())
        res += ';'.join(annot) + '}' + self.form
        return res

    @classmethod
    def from_str(cls, word):
        mo = re.search('^\{(.*)\}(.*)', word)
        if mo:
            form = mo.group(2)
            annot_str = mo.group(1)
            annot = {}
            for kv in annot_str.split(';'):
                k, sep, v = kv.partition('=')
                if sep != '=':
                    continue
                annot[k] = v
        else:
            annot = {}
            form = word
        return cls(annot, form)

    @classmethod
    def update_spelling(cls, tk, new_spelling):
        form = tk.getform()
        annot = tk.getannotations()
        annot['ORIG_ORTH'] = '"%s"' % form
        return cls(annot, new_spelling)

    # TODO merge annotations

    @classmethod
    def merge(cls, tks, comp):
        tk_list = map(lambda x: '"%s"' % x, tks)  # map(lambda x: x.getform(), tks)
        annot = {'ORIG_SEG': '[%s]' % ','.join(tk_list)}
        return cls(annot, comp)

    @classmethod
    def expand(cls, tk, aml):
        annot = tk.getannotations()
        annot['AML'] = '"%s"' % tk.getform()
        return map(lambda x: cls(annot, x), aml)


def levenshtein(w0, w1):
    """
    Computes the Levenshtein distance between two words.
    Source: https://en.wikipedia.org/wiki/Levenshtein_distance
    :param w0: The first word (string).
    :param w1: The second word (string).
    :return: The levenshtein distance between these words (int).
    """
    n0 = len(w0)
    n1 = len(w1)

    if n0 > n1:  # w1 must be longer than w0. Swap the words if necessary.
        w0, w1 = w1, w0
        n0, n1 = n1, n0

    if w0 == w1:
        return 0
    if n0 == 0:
        return n1
    if n1 == 0:
        return n0

    v0 = [x for x in range(n1 + 1)]
    v1 = [0] * (n1 + 1)

    for i in range(n0):
        v1[0] = i + 1
        for j in range(n1):
            cost = 0 if w0[i] == w1[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[i] + cost)
        v0 = list(v1)

    return v1[n1]


def closest_word(candidates, word):
    res_word = None
    min_dist = float('inf')
    for corr in candidates:
        ld = levenshtein(word, corr)
        if ld < min_dist:
            res_word = corr
            min_dist = ld
    return res_word

_amalgams = {
    'du': ['de', 'le'],
    'des': ['de', 'les'],
    'au': ['à', 'le'],
    'aux': ['à', 'les'],
    'duquel': ['de', 'lequel'],
    'desquels': ['de', 'lesquels'],
    'desquelles': ['de', 'lesquelles'],
    'auquel': ['à', 'lequel'],
    'auxquels': ['à', 'lesquels'],
    'auxquelles': ['à', 'lesquelles']
}


def expand_amalgam(word):
    if word in _amalgams:
        return _amalgams[word]
    else:
        return [word]

if __name__ == '__main__':
    import unittest

    class LevenshteinTest(unittest.TestCase):
        def test_equality(self):
            self.assertEqual(levenshtein('mystr', 'mystr'), 0)

        def test_empty_w0(self):
            self.assertEqual(levenshtein('', 'ab'), 2)

        def test_empty_w1(self):
            self.assertEqual(levenshtein('abcd', ''), 4)

        def test_wiki(self):
            """ Uses the examples from the Wikipedia article """
            self.assertEqual(levenshtein('kitten', 'sitting'), 3)
            self.assertEqual(levenshtein('Saturday', 'Sunday'), 3)

    class TokenTests(unittest.TestCase):
        def test_fromstr_simple(self):
            t = Token.from_str('bien')
            self.assertEqual(str(t), 'bien')

        def test_fromstr_withannotations(self):
            t = Token.from_str('{A=a;B=b}bien_sur')
            self.assertEqual(str(t), '{A=a;B=b}bien_sur')

        def test_spellupdate(self):
            t = Token.from_str('{A=a}qautre')
            self.assertEqual(str(Token.update_spelling(t, 'quatre')), '{A=a;ORIG_ORTH="qautre"}quatre')

        def test_merge(self):
            t1 = Token.from_str('quatre')
            t2 = Token.from_str('cinq')
            self.assertEquals(str(Token.merge([t1, t2], 'q_c')), '{ORIG_SEG=["quatre","cinq"]}q_c')

        def test_expand(self):
            t = Token.from_str('{A=a}au')
            l = Token.expand(t, ['a', 'le'])
            self.assertEquals(len(l), 2)
            self.assertEquals(str(l[0]), '{A=a;AML="au"}a')
            self.assertEquals(str(l[1]), '{A=a;AML="au"}le')

    unittest.main()
