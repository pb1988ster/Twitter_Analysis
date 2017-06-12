#Test file to print geo information from tweet json
import json
with open('data/stream_walmart.json', 'r') as f: #walmart1.json is subset of walmart
	counter =0 #index starts from 1 for each tweet 
	print "----------GEO DATA ----------"
	for each in f:
		try:
			tweet=json.loads(each)
			if tweet['coordinates'] != None or tweet['geo']!= None:
				print  tweet['coordinates']
				#print tweet['geo']
				counter+=1
			
		except:pass
print counter
