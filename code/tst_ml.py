#Testing ML algorithm
#Process Training set 
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import csv
import string
#-----------------------------------------Same set of codes used to process tweets for query 
import json
import re
from nltk.corpus import stopwords
from operator import itemgetter
import collections
#----------------------------------------------------
emoticons_str = r"""(?:
[:=;]
[oO\-]? [D\)\]\(\]/\\OpP])"""
regex_str = [
emoticons_str,r'<[^>]+>', # HTML tags
r'(?:@[\w_]+)', # @-mentions
r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
r'(?:[\w_]+)', # other words
r'(?:\S)' # anything else
]
punctuation = list(string.punctuation)
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
#---------------------------------------------------------------------------------------------------
def tokenize(s):
	return tokens_re.findall(s)
def preprocess(s, lowercase=False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

def processTweet(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#----------------------------------------------------------------------------------------------------
feat_bag={}
label=[]
with open('train1.csv', 'r') as f: #location of training data csv file
	flreader = csv.reader(f, delimiter=',')	
	counter =0 #index starts from 1 for each tweet 
	for each in flreader:
		try:
			tweet_txt_clean=(processTweet(str(each[3])))
			label.append(int(each[1]))
			tokens=preprocess(tweet_txt_clean)			
			feat_bag[counter]=tokens
			counter+=1	
		except:pass

cleaned_bag=[]#dictionary of cleaned tweet tokens
stopw = stopwords.words('english')
stopwrd=stopw+punctuation
import unicodedata
stopwrd=[str(x) for x in stopwrd] #convert unicode to strings to avoid invalid comparison errors
for i in range (0,120):
	cleaned_bag.append([word for word in feat_bag[i] if word not in stopwrd]) # puts in format [
print "BAG OF WORDS : --------------------"
print cleaned_bag
#---------------------------------------------------------------------------------------------------------
featureList=[]
lbl=[]
for i in range(0,100):
	featureList=featureList+ list(cleaned_bag[i])
	lbl.append(label[i])
featureList= list(set(featureList))

#-------------------------------------------------------------------
z = zip(cleaned_bag,lbl)
from nltk.tokenize import word_tokenize
train =[({word: (word in word_tokenize(' '.join(x[0]))) for word in featureList}, x[1]) for x in z]
classifier=nltk.NaiveBayesClassifier.train(train)
classifier.show_most_informative_features(8)
#-------------------------------------------------------------------
#Test set 
testarr=[]
#for i in range(101,120):
	#testarr.append(cleaned_bag[i])

#test=[{word: (word in word_tokenize(' '.join(x))) for word in featureList} for x in testarr]
nltk.classify.accuracy(classifier, train)
#print classifier.classify(train)
























