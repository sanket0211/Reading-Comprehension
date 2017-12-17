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
from sklearn.preprocessing import LabelEncoder
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
WINDOW=8
TEST_SIZE=4000
data=""
n_n={}
count=0
for line in f:
	data=data+line[:-1]+". "
	count=count+1
	if count == TEST_SIZE:
		break
#print len(data)
words=[]
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

train_set=[]
train_labels=[]
test_set=[]
test_labels=[]
#print words
for i in range(0,len(words)-WINDOW):
	temp=[]
	for j in range(i,i+WINDOW):
		temp.append(words[j].lower())
	if stem.stemWord(words[i+WINDOW].lower()) not in nouns:
		temp=[]
		continue
	train_set.append(temp)
	train_labels.append(stem.stemWord(words[i+WINDOW].lower()))
#model = Word2Vec(train_set, min_count=1)
#model.save('train_set2.bin')
model = Word2Vec.load('train_set2.bin')
#model = Word2Vec.load('../../word2vec/GoogleNews-vectors-negative300.bin')
lables={}
for i in train_labels:
	if i in lables:
		lables[i]=lables[i]+1
	else:
		lables[i]=1
# for w in sorted(lables, key=lables.get, reverse=True):
# 	if lables[w]>50:
# 		print lables[w],w
temp_train_set=[]
for i in train_set:
	for m in model[i]:
		temp_train_set.append(m)
train_set=temp_train_set
temp_train_set=[]
temp_train_set_small=[]
for i in range(0, len(train_set[0])):
	temp_train_set_small.append(0)
j=0
for i in range(0,len(train_set)):
	j=0
	for m in train_set[i]:
		temp_train_set_small[j]=temp_train_set_small[j]+m
		j=j+1
	j=0
	if (i+1)%WINDOW==0:
		for j in range(0,len(temp_train_set_small)):
			temp_train_set_small[j]=temp_train_set_small[j]/float(WINDOW)
		temp_train_set.append(temp_train_set_small)
		temp_train_set_small=[]
		for k in range(0, len(train_set[0])):
			temp_train_set_small.append(0)
train_set=temp_train_set
count=0
options=[]
for line in o:
	line=line.strip()
	opt=line.split(',')
	options.append(opt)
	count=count+1
	if(count==TEST_SIZE/20):
		break
ind=0
count=0
for i in a:
	test_labels.append(i[:-1].lower())
	count = count+1
	if count==TEST_SIZE/20:
		break
count=0
for line in q:
	line = line.split()
	for i in range(0,len(line)):
		if line[i] == 'XXXXX':
			index_of_missing=i
			if index_of_missing<WINDOW:
				index_of_missing=WINDOW
	temp=[]
	if len(line)<5:
		count=count+1
		temp=line
		test_set.append(temp)
		continue
	for m in range(index_of_missing-WINDOW, index_of_missing):
		temp.append(line[m].lower())
	temp.append('temp')
	#print temp	
	for opt in options[ind]:
		temp[len(temp)-1]=opt
		#print model.score(temp),opt,test_labels[ind]
	test_set.append(temp[:len(temp)-1])
	ind=ind+1
	count = count+1
	if count==TEST_SIZE/20:
		break

sum_ele=0
max_sum=-10
correct=0
incorrect=0
print len(test_set)
print len(options)
for i in range(0,len(test_set)):
	for m in options[i]:
		sum_ele=0
		
		for n in test_set[i]:
			try:
				#print k
				sum_ele = sum_ele + model.similarity(n,m)
			except:
				sum_ele=sum_ele
		if sum_ele>max_sum:
			max_word=m
			max_sum=sum_ele
	print max_word.lower(),test_labels[i]
	print i
	if max_word.lower()==test_labels[i]:
		correct=correct+1
	else:
		incorrect=incorrect+1
print correct
print incorrect
print correct/(correct+incorrect)
exit()

#model = Word2Vec(test_set, min_count=1)
#model.save('test_set22.bin')
#model = Word2Vec.load('../../GoogleNews-vectors-negative300.bin')
#model.save('test_set.bin')
temp_test_set=[]
for i in test_set:
	#print model[i]
	for m in model[i]:
		temp_test_set.append(m)
test_set=temp_test_set

temp_test_set=[]
temp_test_set_small=[]
for i in range(0, len(test_set[0])):
	temp_test_set_small.append(0)
for i in range(0,len(test_set)):
	j=0
	for m in test_set[i]:
		temp_test_set_small[j]=temp_test_set_small[j]+m
		j=j+1
	if (i+1)%(WINDOW)==0:
		for j in range(0,len(temp_test_set_small)):
			temp_test_set_small[j]=temp_test_set_small[j]/float(WINDOW)
		temp_test_set.append(temp_test_set_small)
		temp_test_set_small=[]
		for k in range(0, len(test_set[0])):
			temp_test_set_small.append(0)
test_set=temp_test_set
print len(train_set)
print len(train_labels)
print len(test_set)
print len(test_labels)

# classifier_rbf = svm.SVC(kernel='rbf')
# classifier_rbf.fit(train_set,train_labels)
# prediction_rbf=classifier_rbf.predict(test_set)
# print prediction_rbf
# print(classification_report(test_labels, prediction_rbf))
# print(accuracy_score(test_labels, prediction_rbf))


encoder = LabelEncoder()
encoder.fit(train_labels)
encoded_Y = encoder.transform(train_labels)
dummy_y = np_utils.to_categorical(encoded_Y)
print encoded_Y
print len(dummy_y)
print dummy_y

model = Sequential()
model.add(Dense(1000, input_dim=100, activation='relu'))
model.add(Dense(800, activation='relu'))
model.add(Dense(604, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_set, dummy_y, epochs=5, batch_size=100)

print model
scores = model.evaluate(train_set,dummy_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

#print train_set
#print test_set

