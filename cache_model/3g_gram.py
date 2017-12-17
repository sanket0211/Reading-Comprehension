from __future__ import division
import re
import sys
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
import nltk
from fractions import Fraction

try:
	from Stemmer import Stemmer
except:
	from purestemmer import Stemmer

stem = Stemmer('english')
stop_words = ['.', ',']

DATASET = "../../CBTest/data/cbtest_CN_valid_2000ex.txt"

file = open(DATASET, 'r')

corpus = []
queries = []

def tokenize(line, word_count = {}):
	tokens = []
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
			stemmed_word = word #stem.stemWord(word)
			if word_count.has_key(stemmed_word):
				word_count[stemmed_word] = word_count[stemmed_word] + 1
			else:
				word_count[stemmed_word] = 1
			tokens.append(stemmed_word)
	#print tokens
	return tokens

count = 0
word_count = {}
for l in file.readlines():
	line = l.strip()
	if len(line) > 0 and count < 20:
		sentence = re.sub(r'^\d+ ', "", line)
		corpus.append(tokenize(sentence, word_count))
		count = count + 1

	elif count == 20 and len(line) > 0 and line.find("XXXXX") > 0:
		query = re.sub(r'^\d+ ', "", line)
		queries.append(query)
		count = 0
		word_count.clear()
		#break

#print corpus
print len(corpus)

words_pos_tags = []

for line in corpus:
	words_pos_tags.append(nltk.pos_tag(line))

#print words_pos_tags

bigram_pos_model = {}
trigram_pos_model = {}

for line in words_pos_tags:
	for i in range(len(line)-1):
		bigram_key = (line[i][1], line[i+1][1])
		#print bigram_key
		if bigram_pos_model.has_key(bigram_key) == False:
			bigram_pos_model[bigram_key] = Fraction(1, 1)
		else:
			bigram_pos_model[bigram_key] += Fraction(1, 1)

		if i < len(line)-2:
			trigram_key = (line[i][1], line[i+1][1], line[i+2][1])
			#print trigram_key
			if trigram_pos_model.has_key(trigram_key) == False:
				trigram_pos_model[trigram_key] = Fraction(1, 1)
			else:
				trigram_pos_model[trigram_key] += Fraction(1, 1)

print bigram_pos_model
print trigram_pos_model

def predict(query):
	parts = [ i.strip() for i in query.split("\t") if len(i) > 0 ]
	parts_len = len(parts)
	answer = parts[parts_len-2]
	options = [ i.lower() for i in parts[parts_len-1].split("|") ]

	query_tokens = tokenize(parts[0])
	#print query_tokens

	predicted = {}
	predicted['val'] = ""
	predicted['prob'] = 0

	blank_index = query_tokens.index("xxxxx")
	if blank_index < 2:
		return False

	lite = nltk.pos_tag(query_tokens[blank_index-2:blank_index])

	for option in options:
		option_tag = nltk.pos_tag([option])
		nlite = lite + option_tag
		#print nlite

		numo = tuple([i[1] for i in nlite])
		deno = tuple([i[1] for i in lite])

		try:
			prob = trigram_pos_model[numo]/bigram_pos_model[deno]
		except KeyError:
			prob = 0

		print prob, option
		if prob > predicted['prob']:
			predicted['val'] = option
			predicted['prob'] = prob

	if answer != predicted['val']:
		print answer, predicted['val']

	print "-------"

	return answer == predicted['val']

match_count = 0
for query in queries:
	print query
	if predict(query):
		match_count = match_count + 1

print "Accuracy: ", match_count/len(queries)

