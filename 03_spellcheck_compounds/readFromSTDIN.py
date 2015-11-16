#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : JTanon

import io
import sys
import cPickle as pickle

lefff = pickle.load(open('lefff_pickle.p', 'r'))
input_stream = raw_input()

pref = input_stream[0]
if pref in lefff:
	for el in lefff[pref]:
		print el.decode('utf-8')
