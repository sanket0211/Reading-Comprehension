import nltk
import string
import sys
import re

from contractions import *
from fractions import Fraction

window_size = 7;
train_sentences = 1000000;
test_sentences = 44000;

#DATASET = "../../CBTest/data/cbtest_CN_valid_2000ex.txt"
DATASET = "../../CBTest/data/cbtest_V_train.txt";
TESTSET = "../../CBTest/data/cbtest_V_valid_2000ex.txt";
Discounting_factor = Fraction(1,2);

ngrams_model = [];
ngram_total_count = [];
unique_follow_counts = {};

query_sentences = [];
query_options = [];
query_answers = [];
query_predicted = [];

for i in range(0,window_size+1):
    ngrams_model.append({});
    ngram_total_count.append(0);

filetrain = open(DATASET,'r');
filetest = open(TESTSET,'r');

def kneserney(last_word,ngram):

    global ngrams_model,ngram_total_count,unique_follow_counts,query_sentences,query_options,query_answers,query_predicted;

    if len(ngram)==0:
        if ( unique_follow_counts.has_key(tuple([last_word])) == False):
            print "no fou", last_word;
            return 0;
        return unique_follow_counts[tuple([last_word])]/Fraction(len(ngrams_model[2].keys()),1);

    term1 = 0;
    if ngrams_model[len(ngram)+1].has_key(tuple(ngram+[last_word])):
        term1 = (ngrams_model[len(ngram)+1][tuple(ngram+[last_word])]-Discounting_factor)/ngram_total_count[len(ngram)+1];

    term2 = 0;
    if (unique_follow_counts.has_key(tuple(ngram))):
        term2 = (Discounting_factor*(unique_follow_counts[tuple(ngram)]))/(ngram_total_count[len(ngram)+1])*kneserney(last_word,ngram[0:len(ngram)-1]);
    return term1+term2;

def set_unique_follow():

    global ngrams_model,ngram_total_count,unique_follow_counts,query_sentences,query_options,query_answers,query_predicted;

    for window in range(2,window_size+1):
        for ngram_key in ngrams_model[window].keys():
            new_ngram = tuple(list(ngram_key[0:len(ngram_key)-1]));
            if unique_follow_counts.has_key(new_ngram):
                unique_follow_counts[new_ngram]+=Fraction(1,1);
            else :
                unique_follow_counts[new_ngram]=Fraction(1,1);


def generate_ngram_model():

    global ngrams_model,ngram_total_count,unique_follow_counts,query_sentences,query_options,query_answers,query_predicted;

    for i in range(0,train_sentences):
        if (i%1000==0):
            print i;
        sentence = filetrain.readline();
        sentence = sentence.lower();
        sentence = sentence.replace('\n','');
        sentence = re.sub('[^A-Za-z0-9|\s]',' ', sentence)
        if (len(sentence)<1):
            continue;
        tokens = nltk.word_tokenize(sentence);
        tokens.pop(0);

        if (sentence.find("xxxxx")!=-1):
            continue;

        for token in tokens :
            if token in contractions:
                token = contractions[token];

        for window in range(1,window_size+1):
            for position in range(0,len(tokens)+1-window):
                sub_tokens = tokens[position:position+window];
                if (ngrams_model[window].has_key(tuple(sub_tokens)))==False:
                    ngrams_model[window][tuple(sub_tokens)]=Fraction(1,1);
                else :
                    ngrams_model[window][tuple(sub_tokens)]+=Fraction(1,1);


    for window in range(1,window_size+1):
        ngram_total_count[window] = Fraction( (sum(ngrams_model[window][x] for x in ngrams_model[window].keys() )),1);

def predict_answers():

    global ngrams_model,ngram_total_count,unique_follow_counts,query_sentences,query_options,query_answers,query_predicted;

    print "raj manvar";
    print len(query_sentences);
    for sentence_i in range(0,len(query_sentences)):
        inde = query_sentences[sentence_i].index("xxxxx");
        previous_context = query_sentences[sentence_i][inde-window_size+1:inde];
        options_list = query_options[sentence_i].split('|');
        predicted_probabilities = [];
        for option in options_list :
            probability = kneserney(option,previous_context);
            predicted_probabilities.append((probability,option));
        predicted_probabilities.sort();
        print predicted_probabilities;
        query_predicted.append(predicted_probabilities[len(predicted_probabilities)-1][1]);


def set_questions():

    global ngrams_model,ngram_total_count,unique_follow_counts,query_sentences,query_options,query_answers,query_predicted;

    for i in range(0,test_sentences):
        sentence = filetest.readline();
        sentence = sentence.lower();
        sentence = sentence.replace('\n','');
        sentence = re.sub('[^A-Za-z0-9|\s]',' ', sentence)
        if (len(sentence)<1):
            continue;
        tokens = nltk.word_tokenize(sentence);
        tokens.pop(0);

        if (sentence.find("xxxxx")!=-1):
            query_options.append(tokens[len(tokens)-1]);
            query_answers.append(tokens[len(tokens)-2]);
            query_sentences.append(tokens[0:len(tokens)-2]);
            continue;


generate_ngram_model();
set_unique_follow();
set_questions();
predict_answers();
denominator = len(query_predicted);
numerator = 0;
for i in range(0,len(query_answers)):
    if (query_answers[i]==query_predicted[i]):
        numerator = numerator+1;

print query_answers;
print query_predicted;
print numerator,denominator;
accuracy = Fraction(numerator,denominator);
print accuracy;

# print query_predicted;
# print query_answers;
# print query_options;
# print ngram_total_count;
# print kneserney("us",["they"]);
