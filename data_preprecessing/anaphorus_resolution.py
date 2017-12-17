import nltk
import re
import sys
from copy import deepcopy
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")

from corenlp import *
import json
reload(sys)
sys.setdefaultencoding('utf-8')

stop_words = ['.', ',']

#DATASET = "../CBTest/data/cbtest_CN_valid_2000ex.txt"
DATASET = "../CBTest/data/cbtest_CN_train.txt"

file = open(DATASET, 'r')

corpus = []
context = []
queries = []	
frequencies = []
lines = []

lines2=[]

count = 0
word_count = {}
for line in file.readlines():
	if len(line) > 0 and count < 20:
		line = re.sub(r'^\d+ ', "", line)
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
		line = re.sub( '\s+', ' ', line).strip()
		lines.append(line)
		#context.append(tokenize(sentence, word_count))
		count = count + 1

	elif count == 20 and len(line) > 0 and line.find("XXXXX") > 0:
		line = re.sub(r'^\d+ ', "", line)
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
		line = re.sub( '\s+', ' ', line).strip()
		queries.append(line)
		count=count+1
		frequencies.append(deepcopy(word_count))
		word_count.clear()
		corpus.append(context)
		#break
	elif count == 21:
		count=0

string_data=""

f=open('processed_data_train.txt', 'wa+')
corenlp = StanfordCoreNLP()  # wait a few minutes...
print len(lines)
for j in range(0,len(lines)):
	#print h
	string_data = string_data + lines[j]
	string_data = string_data + ". "
	lines2.append(str(lines[j]))
	#print string_data, j
	if((j+1)%20==0):
		print j
		try:
			ana_res = json.loads(corenlp.parse(string_data))['coref']
		except Exception as e:
    		#handle_the_exception_error
			print string_data
			lines3=[]
			string_data=""
			for i in lines2:
				temp_str=""
				pos_tags_tokens = nltk.word_tokenize(i)
				pos_tags = nltk.pos_tag(pos_tags_tokens)
				for m in pos_tags_tokens:
					for n in pos_tags:
						if n[0]==m:
							m = m + '/'+n[1]
							temp_str=temp_str+m + " "
							break
				lines3.append(temp_str)
			lines2=lines3
			for i in lines2:	
				f.write(i)
				f.write('\n')
			lines2=[]	
			continue
#print "step3"
		string_data=""
		#print ana_res
		for i in ana_res:
			for j in i:
				word1 = j[0][0];
				sentence = j[0][1];
				word2 = j[1][0];
				words = lines2[sentence].split()
				s1=""
				for w in words:
					if w==word1:
						w = word2
					s1 = s1 + w
					s1 = s1 + " "
				lines2[sentence] = s1
		lines3=[]
		for i in lines2:
			temp_str=""
			pos_tags_tokens = nltk.word_tokenize(i)
			pos_tags = nltk.pos_tag(pos_tags_tokens)
			#print pos_tags
			for m in pos_tags_tokens:
				for n in pos_tags:
					if n[0]==m:
						m = m + '/'+n[1]
						temp_str=temp_str+m + " " 
						break
			lines3.append(temp_str)
		lines2=lines3
		#print lines2
		for i in lines2:
			f.write(i)
			f.write('\n')
		lines2=[]	





#print json.loads(corenlp.parse(string_data))['coref'][0]
