'''
Created on May 19, 2013

@author: phil
'''
import ConfigParser
import tweepy

config = ConfigParser.ConfigParser()
config.read("/home/phil/twitter_keys.config")
# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = config.get('Keys', 'consumer_key')
consumer_secret = config.get('Keys', 'consumer_secret')

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token = config.get('Keys', 'access_token')
access_token_secret = config.get('Keys', 'access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def getTweetsFromUser(username):
    tweetsString = ""
    last_id = None
    while True:
        # fetch 200 tweets at a time
        tweets = api.user_timeline(screen_name = username, count = 200, max_id = last_id)
        if not tweets:
            # there are no tweets left
            break
        # append the current tweets to tweetsString
        tweetsString = "".join((tweetsString, "".join([" ".join([tweet.text.encode('utf8').lower(), "ENDTWEET\n"]) for tweet in tweets])))
        last_id = tweet.id - 1
    return tweetsString