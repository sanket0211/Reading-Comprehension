from __future__ import division
import re
import sys
from copy import deepcopy
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
import nltk
from Stemmer import Stemmer 


stem = Stemmer('english')
stop_words = ['.', ',']

DATASET = "../../CBTest/data/cbtest_CN_valid_2000ex.txt"

file = open(DATASET, 'r')

corpus = []
context = []
queries = []
frequencies = []
lines = []

def tokenize(line, word_count):
	# TODO: Handle apostrophe
	tokens = []
	#words = [ j.strip() for j in re.compile(r'[^A-Za-z\-]+').split(line.lower()) if len(j) > 0 ]
	line = re.sub('n[\']t',' not',line)
	line = re.sub('[\s\n]ca ',' can ', line)
	line = re.sub(' [\']ll',' will', line)
	line = re.sub(' [\']s',' is', line)
	line = re.sub(' [\']m',' am', line)
	line = re.sub(' [\']d',' would', line)
	line = re.sub(' [\']ve',' have', line)
	line = re.sub(' [\']re',' are', line)	
	line = re.sub('http : //.*?[\n\s]',' URL ', line)
	line = re.sub('https : //.*?[\n\s]','URL ', line)
	line = re.sub('[^A-Za-z0-9\s]',' ', line)
	words = nltk.word_tokenize(line.lower())
	#print words
	for word in words:
		if word not in stop_words:
			stemmed_word = stem.stemWord(word)
			if word_count.has_key(stemmed_word):
				word_count[stemmed_word] = word_count[stemmed_word] + 1
			else:
				word_count[stemmed_word] = 1
			tokens.append(stemmed_word)
	#print tokens
	return tokens

count = 0
word_count = {}
for line in file.readlines():
	if len(line) > 0 and count < 20:
		sentence = re.sub(r'^\d+ ', "", line)
		lines.append(sentence)
		context.append(tokenize(sentence, word_count))
		count = count + 1

	elif count == 20 and len(line) > 0 and line.find("XXXXX") > 0:
		query = re.sub(r'^\d+ ', "", line)
		queries.append(query)
		count=count+1
		frequencies.append(deepcopy(word_count))
		word_count.clear()
		corpus.append(context)
		#break
	elif count==21:
		count=0

print len(context)
print len(queries)
print len(corpus)
print len(frequencies)

def predict(query, frequency):
	global context_count
	parts = [ i.strip() for i in query.split("\t") if len(i) > 0 ]
	parts_len = len(parts)
	answer = parts[parts_len-2]
	options = [ stem.stemWord(i.lower()) for i in parts[parts_len-1].split("|") ]

	predicted = {}
	predicted['val'] = ""
	predicted['freq'] = 0

	for option in options:
		if frequency.has_key(option):
			count = frequency[option]
			if count > predicted['freq']:
				predicted['freq'] = count
				predicted['val'] = option

	# if answer != predicted['val']:
	# 	print answer
	# 	print predicted

	return answer == predicted['val']

#print frequencies

print "MAXIMUM FREQUENCY (CONTEXT) RESULT"
print "----------------------------------"

context_match_count = 0
for i in range(len(queries)):
	if predict(queries[i], frequencies[i]):
		context_match_count = context_match_count + 1
	pass

print "Accuracy: ", context_match_count/len(queries)

corpus_frequency = {}
for frequency in frequencies:
	for key in frequency.keys():
		if corpus_frequency.has_key(key):
			corpus_frequency[key] = corpus_frequency[key] + frequency[key]
		else:
			corpus_frequency[key] = frequency[key]

#print len(corpus_frequency)
#print corpus_frequency

print "MAXIMUM FREQUENCY (CORPUS) RESULT"
print "----------------------------------"

corpus_match_count = 0
for i in range(len(queries)):
	if predict(queries[i], corpus_frequency):
		corpus_match_count = corpus_match_count + 1

print "Accuracy: ", corpus_match_count/len(queries)
