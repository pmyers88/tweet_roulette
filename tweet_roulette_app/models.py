from django.db import models
from nltk.tokenize.regexp import RegexpTokenizer
from collections import defaultdict
from random import choice

class BlobField(models.Field):
    description = "MediumBlob"
    def db_type(self, connection):
        return 'mediumblob'

class TwitterAccount(models.Model):
    username = models.CharField(max_length=15, unique = True)
    textCorpus = BlobField()
    lastUpdated = models.DateField(auto_now=True)
    
    def generateTweet(self, n):
        ngramDict = defaultdict(list)
        startTweets = []
        tokenizer = RegexpTokenizer("[@#$]?\w+(['-_:/.]+\w+)*") 
        tokenizedCorpus = [tokenizer.tokenize(tweet) for tweet in self.textCorpus.split("ENDTWEET")]
        
        # get the list of tuples that are the first n words of a tweet
        for tweet in tokenizedCorpus:
            startTweets.append(tuple(tweet[0:n]))
            tweet.append("")
            [ngramDict[tuple(tweet[i:i+n])].append(tweet[i+n]) for i in range(len(tweet) - n)]
    
        key = choice(startTweets)
        tweet = list(key)
        tweetLength = len(" ".join(tweet))
        if "" not in key:
            while True:
                word = choice(ngramDict[key])
                tweetLength += len(word) + 1
                if tweetLength <= 140 and word:
                    tweet.append(word)
                    key = key[1:] + (word,)
                else:
                    break
        return " ".join(tweet)
    
    def __unicode__(self):
        return u'Username: %s; Last Updated: %s'  % (self.username, self.last_updated)
