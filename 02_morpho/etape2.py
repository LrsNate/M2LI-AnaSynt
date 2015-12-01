#!/usr/bin/python
# -*- coding: utf-8 -*-

import morpho as m
from morpho import defloat
import fileinput as fi
from functools import partial

w=m.importweights("weights.pickle")
k=m.importweights("known.pickle")
taggit=m.memoize(lambda x: partial(m.classify,w)(m.getfeatures(x)))

for line in fi.input():
	line=line.strip()
	if line not in k and line != "":
		print line,taggit(line.decode("utf-8"))
	else:
		pass

