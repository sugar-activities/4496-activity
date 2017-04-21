#!/usr/bin/env python

# Given a string of the form (x, y), return a tuple
# consisting of the x,y values as integers.
def ScanPair(s) :
	sp = s.split(',')
	return (int(sp[0]), int(sp[1]))
	
# Add the values in two tuples together
def AddTuples(a, b) :
	return (a[0] + b[0], a[1] + b[1])

def SubTuples(a, b) :
	return (a[0] - b[0], a[1] - b[1])