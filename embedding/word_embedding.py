import os
import numpy as np
import time ,random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.pipeline import FeatureUnion
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import pandas
from Stemmer import Stemmer 

stem = Stemmer('english')
stop_words = ['.', ',']

stop_words = set(stopwords.words('english'))
stop_words.add('.')
stop_words.add('I')

f = open('../../data/processed_data.txt', 'r')
q = open('../../data/queries.txt', 'r')
o = open('../../data/options.txt', 'r')
a = open('../../data/answers.txt', 'r')
tmp =  open('tmp.txt', 'wa+')
nouns=[]
WINDOW=7
TEST_SIZE=40000
data=""
n_n={}
correct=0
incorrect=0
count=0

test_labels=[]
test_set=[]
for i in a:
	test_labels.append(i[:-1].lower())


options=[]
for line in o:
	line=line.strip()
	opt=line.split(',')
	options.append(opt)


for line in q:
	line = line.split()
	for i in range(0,len(line)):
		if line[i] == 'XXXXX':
			index_of_missing=(i+WINDOW/2+1)
			if index_of_missing<WINDOW:
				index_of_missing=WINDOW
	temp=[]
	if len(line)<(WINDOW+1):
		temp=line
		test_set.append(temp)
		continue
	for m in range(index_of_missing-WINDOW, index_of_missing):
		#print len(line)
		#print m
		try:
			temp.append(line[m].lower())
		except:
			continue
	print temp
	test_set.append(temp)

index=0

for line in f:
	print index
	data=data+line[:-1]+". "
	count=count+1
	if count%20==0:
		words=[]
		nouns=[]
		for t in data.split():
			#print nltk.tag.str2tuple(t)[1]
			try:
				if nltk.tag.str2tuple(t)[1][0]=='N':
					#no_of_nouns=no_of_nouns+1
					#n_n[stem.stemWord(nltk.tag.str2tuple(t)[0].lower())]=1
					nouns.append(stem.stemWord(nltk.tag.str2tuple(t)[0].lower()))
			except:
				g=1
			words.append(nltk.tag.str2tuple(t)[0].lower())

		data=""
		train_set=[]
		train_labels=[]
		
		for i in range(0,len(words)-WINDOW):
			temp=[]
			for j in range(i,i+WINDOW):
				temp.append(words[j].lower())
			if stem.stemWord(words[i+WINDOW].lower()) not in nouns:
				temp=[]
				continue
			train_set.append(temp)
			train_labels.append(stem.stemWord(words[i+WINDOW].lower()))
		model = Word2Vec(train_set, min_count=1)
		#print train_set
		sum_ele=0
		max_sum=-10
		for m in options[index]:
			sum_ele=0
			
			for n in test_set[index]:
				try:
					#print n,m,(model.similarity(n,m))
					#print sum_ele
					sum_ele = sum_ele + model.similarity(n,m)
				except:
					sum_ele=sum_ele
			#print m,sum_ele
			if sum_ele>max_sum:
				max_word=m
				max_sum=sum_ele
		#print max_word.lower()
		#print test_labels[index]
		#print test_set[index]
		if max_word.lower()==test_labels[index]:
			correct=correct+1
		else:
			incorrect=incorrect+1
		index=index+1

print correct
print incorrect