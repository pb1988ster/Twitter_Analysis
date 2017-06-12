#Author-Pulkit Bhardwaj
#Code to read each line from json file containing twitter data , remove stop words ,Form tags in each and form bag of words
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
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
def tokenize(s):
	return tokens_re.findall(s)
def preprocess(s, lowercase=False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens
#---------------------------------------------------
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

#-------------------------------------------------
bag_of_words={}
with open('data/stream_walmart.json', 'r') as f: #walmart1.json is subset of walmart
	counter =0 #index starts from 1 for each tweet 
	for each in f:
		try:
			tweet=json.loads(each)
			tweet_txt_clean=processTweet(tweet['text'])
			tokens=preprocess(tweet_txt_clean)			
			bag_of_words[counter]=tokens
			counter+=1
			
		except:pass
#-------------------------------------------------
import string
punctuation = list(string.punctuation)
stopw = stopwords.words('english')
sstop=["walmart","wmart"] #specific stopwords for walmart analysis
stopw=stopw+punctuation+sstop
stopwordsfree_words={}
for i in range (0,5000):
	stopwordsfree_words[i] = [word for word in bag_of_words[i] if word not in stopw]

#--------------------------------------------------
#pickle is used to write data and read it later - thus freeing memory 
import pickle
pickle.dump(stopwordsfree_words, open("bow_file.txt", 'wb'))
yourDict = pickle.load(open("bow_file.txt", 'rb'))
#------------------------------------------------
#Top things people write in tweets
ss=[]
for i in range(0,5000):
	ss.append(yourDict[i])
import itertools
ss=list(itertools.chain(*ss))
from collections import defaultdict
fq= defaultdict( int )
arr1=[]
for w in ss:
    fq[w] += 1
for key, value in  sorted(fq.iteritems(), key=lambda (k,v): (v,k),reverse=True):
	if value>50:    #specify a base frequency that is significant
		#print "%s: %s" % (key, value)
		arr1.append(key)
print "-------------Top words in tweets----------------------------" 
print arr1
#----------------------------------------------------------------------------------------
#Making geo location data	
# Tweets are stored in "fname"
with open('data/stream_walmart.json', 'r') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)
print "--------------Geo Tag data -----------"
print geo_data 
print"SAVING GEO DATA -----------------------------------"
# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))


