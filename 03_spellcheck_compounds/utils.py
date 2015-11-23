#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import cPickle as pickle


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


# int LevenshteinDistance(string s, string t)
# {
#     // degenerate cases
#     if (s == t) return 0;
#     if (s.Length == 0) return t.Length;
#     if (t.Length == 0) return s.Length;
#
#     // create two work vectors of integer distances
#     int[] v0 = new int[t.Length + 1];
#     int[] v1 = new int[t.Length + 1];
#
#     // initialize v0 (the previous row of distances)
#     // this row is A[0][i]: edit distance for an empty s
#     // the distance is just the number of characters to delete from t
#     for (int i = 0; i < v0.Length; i++)
#         v0[i] = i;
#
#     for (int i = 0; i < s.Length; i++)
#     {
#         // calculate v1 (current row distances) from the previous row v0
#
#         // first element of v1 is A[i+1][0]
#         //   edit distance is delete (i+1) chars from s to match empty t
#         v1[0] = i + 1;
#
#         // use formula to fill in the rest of the row
#         for (int j = 0; j < t.Length; j++)
#         {
#             var cost = (s[i] == t[j]) ? 0 : 1;
#             v1[j + 1] = Minimum(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost);
#         }
#
#         // copy v1 (current row) to v0 (previous row) for next iteration
#         for (int j = 0; j < v0.Length; j++)
#             v0[j] = v1[j];
#     }
#
#     return v1[t.Length];
# }
def levenshtein(s, t):
    if s == t:
        return 0

    len_s = len(s)
    len_t = len(t)

    if len_s == 0:
        return min(3, len_t)
    if len_t == 0:
        return min(3, len_s)

    v0 = [x for x in range(len_t + 1)]
    v1 = [0] * (len_t + 1)

    for i in range(len_s):
        v1[0] = i + 1
        for j in range(len_t):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            if v1[j + 1] > 2:
                return 42
        v0 = list(v1)
    return v1[len_t]

# def levenshtein(w0, w1, len0, len1):
#     if len0 == 0:
#         return len1
#     if len1 == 0:
#         return len0
#
#     if w0[len0 - 1] == w1[len1 - 1]:
#         cost = 0
#     else:
#         cost = 1
#
#     return min(levenshtein(w0, w1, len0 - 1, len1) + 1,
#                levenshtein(w0, w1, len0, len1 - 1) + 1,
#                levenshtein(w0, w1, len0 - 1, len1 - 1) + cost)


def closest_word(candidates, word):
    res_word = None
    min_dist = float('inf')
    for corr in candidates:
        ld = levenshtein(word, corr)
        if ld < min_dist and ld <= 2:
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

_keyboard_probabilities = {
    'a': {'z':.5, 'q':.35, 's':.15},
    'z': {'a':.21, 'e':.28, 'q':.15 , 's':.21, 'd':.15},
    'e': {'z':.25, 'r':.25, 's':.18, 'd':.22, 'f':.10},
    'r': {'e':.25, 't':.25, 'd':.18, 'f':.22, 'g':.10},
    't': {'r':.25, 'y':.25, 'f':.18, 'g':.22, 'h':.10},
    'y': {'t':.25, 'u':.25, 'g':.18, 'h':.22, 'j':.10},
    'u': {'y':.25, 'i':.25, 'h':.18, 'j':.22, 'k':.10},
    'i': {'u':.25, 'o':.25, 'j':.18, 'k':.22, 'l':.10},
    'o': {'i':.25, 'p':.25, 'k':.18, 'l':.22, 'm':.10},
    'p': {'o':.30, 'l':.40, 'm':.30},
    'q': {'s':.30, 'a':.40, 'w':.30},
    's': {'a':.10, 'z':.15, 'e':.10, 'q':.20, 'd':.20, 'w':.10, 'x':.15},
    'd': {'z':.10, 'e':.15, 'r':.10, 's':.20, 'f':.20, 'x':.10, 'c':.15},
    'f': {'e':.10, 'r':.15, 't':.10, 'd':.20, 'g':.20, 'c':.10, 'v':.15},
    'g': {'r':.10, 't':.15, 'y':.10, 'f':.20, 'h':.20, 'v':.10, 'b':.15},
    'h': {'t':.10, 'y':.15, 'u':.10, 'g':.20, 'j':.20, 'b':.10, 'n':.15},
    'j': {'y':.10, 'u':.15, 'i':.10, 'h':.20, 'k':.20, 'n':.10, ',':.15},
    'k': {'u':.10, 'i':.15, 'o':.10, 'j':.20, 'l':.20, ',':.10, ';':.15},
    'l': {'i':.10, 'o':.15, 'p':.10, 'k':.20, 'm':.20, ';':.10, ':':.15},
    'm': {'o':.05, 'p':.10, 'l':.25, 'ù':.25, ':':.15, '!':.20},
    'w': {'q':.05, 's':.20, 'x':.40, '<':.35},
    'x': {'w':.35, 's':.20, 'd':.10, 'c':.35},
    'c': {'x':.35, 'd':.20, 'f':.10, 'v':.35},
    'v': {'c':.35, 'f':.20, 'g':.10, 'b':.35},
    'b': {'v':.35, 'g':.20, 'h':.10, 'n':.35},
    'n': {'b':.35, 'h':.20, 'j':.10, ',':.35}
}


_lefff = pickle.load(open('lefff_pickle.p', 'r'))


def get_candidates_from_lefff(word):
    """
    Extracting words with same prefix from lefff
    """
    try:
        tmp_candidates = _lefff[word[0].lower().strip()]
        return refine_candidates(word, tmp_candidates)
    except KeyError:
        return []


def refine_candidates(word, candidates):
    best_candidates = []
    for candidate in candidates:
        if abs(len(candidate) - len(word)) < 2:
            best_candidates.append(candidate)
    return best_candidates


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
            self.assertEqual(levenshtein('abcd', ''), 3)

        def test_wiki(self):
            """ Uses the examples from the Wikipedia article. Basically, 3 = a lot. """
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
