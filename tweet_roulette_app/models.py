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
        
        for tweet in tokenizedCorpus:
            # don't use tweets that aren't long enough to add to ngramDict
            if len(tweet) >= n:
                # add padding to the start of the tweet
                tweet.insert(0, 'START')
                # need to add this so that ngrams can be formed from the last n words of a tweet
                tweet.append("")
                startTuple = tuple(tweet[0:n])
                # create a list of tuples that are the first n-1 words of a tweet
                # this is done so that the generated tweets make more sense and have more variety
                startTweets.append(startTuple)
                # create the dictionary of n-grams to the list of words following each n-gram
                ngramDict[startTuple].append(tweet[n])
                for i in range(1, len(tweet) - n):
                    dictKey = tuple(tweet[i:i+n])
                    ngramDict[dictKey].append(tweet[i+n])

        print len(ngramDict)

        # the start of a generated tweet is always the start of a tweet from the corpus
        key = choice(startTweets)
        tweet = list(key)
        #remove the dummy start word
        tweet.remove('START')
        tweetLength = len(" ".join(tweet))
        if "" not in key:
            while True:
                # select one of the words mapped to the current ngram key
                word = choice(ngramDict[key])
                tweetLength += len(word) + 1
                if tweetLength <= 120 and word:
                    tweet.append(word)
                    key = key[1:] + (word,)
                else:
                    break
        return " ".join(tweet)
    
    def __unicode__(self):
        return u'Username: %s; Last Updated: %s'  % (self.username, self.lastUpdated)