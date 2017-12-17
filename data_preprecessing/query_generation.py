from __future__ import division
import re
import sys
from copy import deepcopy
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
import nltk
from Stemmer import Stemmer 


stem = Stemmer('english')
stop_words = ['.', ',']

DATASET = "../CBTest/data/cbtest_CN_valid_2000ex.txt"


f = open('queries.txt', 'r')
g = open('queries2.txt', 'wa+')

query_str=""

#l = open('options.txt', 'r')
A = open('queries2.txt','wa+')
l=[]
for line in f:
	#print line.find(line2)	
	l = line.split()
	#A.write(l[len(l)-2])
	#A.write('\n')
	string = ""
	m = 0
	for m in range(0,len(l)):
		if m == len(l)-2:
			break
		string = string + l[m] + " "
		m = m+1
	g.write(string)
	g.write('\n')