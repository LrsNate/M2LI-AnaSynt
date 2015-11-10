#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from collections import defaultdict, Counter


def extract_root_and_children(buf):
    brackets_balance = 0
    seq = []
    segm_in_process = ''

    for char in buf:
        if char == '(':
            brackets_balance += 1
        elif char == ')':
            brackets_balance -= 1
        if brackets_balance == 0 and char == ' ':
            seq.append(segm_in_process)
            segm_in_process = ''
        else:
            segm_in_process += char

    if brackets_balance == -1:
        seq.append(segm_in_process[:-1])
    else:
        seq.append(segm_in_process)
    return seq[0], seq[1:]


def extract_rules(line, rules, lexicon):
    root, children = extract_root_and_children(line)
    right = []
    for child in children:
        child = child[1:-1]
        if '(' not in child:
            pos, word = child.split()
            lexicon.append(word + "\t" + pos)
            right.append(pos)
        else:
            left = extract_rules(child, rules, lexicon)
            right.append(left)
    rules[root].append(tuple(right))
    return root

if __name__ == '__main__':
    # sys.setrecursionlimit(5000)
    trainset = open("ftb6_2.mrg")
    rules = defaultdict(list)
    lexicon = []
    for line in trainset:
        extract_rules("ROOT" + line[1:-1], rules, lexicon)
    pcfg = {'left': []}
    for left, right in rules.items():
        lst = [(rule, count / len(right))
               for rule, count in Counter(right).items()]
        pcfg['left'].append(lst)
