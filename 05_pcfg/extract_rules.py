#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import shelve
import re
from collections import defaultdict,Counter

def extract_root_and_children(buf,brackets_balance,seq, segm_in_process):
	if len(buf)==0:
		#PB : Cette condition ne devrait pas être nécessaire... 
		#Pourquoi y a-t-il une parenthèse fermante en trop à la fin de la phrase?? A vérifier !!
		if brackets_balance == -1:
			seq+=[segm_in_process[:-1]]
		else:
			seq+=[segm_in_process]
		return seq[0],seq[1:]
	else :
		char = buf[0]
		if char == '(':
			brackets_balance += 1
		elif char == ')':
			brackets_balance -= 1
		if brackets_balance == 0 and char == ' ':
			return extract_root_and_children(buf[1:],brackets_balance,seq+[segm_in_process],"")
		else :
			return extract_root_and_children(buf[1:],brackets_balance,seq,segm_in_process+char)

def extract_rules(line,rules,lexicon):
	root,children = extract_root_and_children(line,0,[],"")
	right = []
	for child in children :
		child = child[1:-1]
		if '(' not in child :
			pos,word = child.split()
			lexicon.append(word+"\t"+pos)
			right.append(pos)
		else :
			left = extract_rules(child,rules,lexicon)
			right.append(left)
	rules[root].append(tuple(right))
	return root

if __name__== '__main__':
	sys.setrecursionlimit(5000)
	trainset = open("ftb6_2.mrg")
	rules    = defaultdict(list)
	lexicon  = []
	for line in trainset :
		extract_rules("ROOT"+line[1:-1],rules,lexicon)
	pcfg     = {left:[(rule,count/len(right)) for rule,count in Counter(right).items()]for left,right in rules.items()}
