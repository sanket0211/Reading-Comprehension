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

l = open('options.txt', 'wa+')

for line in f:
	#print line
	length = len(line)
	i = length-1
	temp=""
	options=[]
	while i>=0:
		#print line[i]
		#print i
		if line[i]=='|':
			options.append(temp)
			temp=""
			i = i-1
		elif line[i]==" ":
			opt_str=""
			#print temp
			temp2=""
			for s in temp:
				if s<='z' and s>='a':
					temp2=temp2+s
				elif s<='Z' and s>='A':
					temp2=temp2+s
				else:
					break
			temp=temp2
			options.append(temp)
			for m in options:
				opt_str = opt_str + m + ","
			opt_str = opt_str[::-1]
			opt_str = opt_str[1:]
			print opt_str
			l.write(opt_str)
			
			i = i - 1
			break
		else:
			temp = temp + line[i]
			i = i - 1
	#print line
	#break
	#h.write(line)

