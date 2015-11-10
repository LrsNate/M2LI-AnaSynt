#!/usr/bin/env python3


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

    unittest.main()
