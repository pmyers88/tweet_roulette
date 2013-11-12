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
        # tokenizes URLs, other twitter lingo (@shaq #awesome), and normal words
        tokenizer = RegexpTokenizer("[@#$]?\w+(['-_:/.]+\w+)*") 
        # creates a list of tokenized tweets; didn't want to just create one big corpus so that
        # the frequency of words that start a tweet can be retained
        tokenizedCorpus = [tokenizer.tokenize(tweet) for tweet in self.textCorpus.split("ENDTWEET")]
        
        # get the list of tuples that are the first n words of a tweet
        for tweet in tokenizedCorpus:
            if len(tweet) >= n:
                startTweets.append(tuple(tweet[0:n]))
                # need to add this so that ngrams can be formed from the last n words of a tweet
                tweet.append("")
                for i in range(len(tweet) - n):
                    dictKey = tuple(tweet[i:i+n])
                    ngramDict[dictKey].append(tweet[i+n])
    
        # the start of a generated tweet is always the start of a tweet from the corpus
        key = choice(startTweets)
        print key
        tweet = list(key)
        tweetLength = len(" ".join(tweet))
        if "" not in key:
            while True:
                # select one of the words mapped to the current ngram key
                word = choice(ngramDict[key])
                tweetLength += len(word) + 1
                if tweetLength <= 140 and word:
                    tweet.append(word)
                    key = key[1:] + (word,)
                else:
                    break
        print tweet
        return " ".join(tweet)
    
    def __unicode__(self):
        return u'Username: %s; Last Updated: %s'  % (self.username, self.last_updated)