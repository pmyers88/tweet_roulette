import ConfigParser
import tweepy

def getAPI():
    config = ConfigParser.ConfigParser()
    config.read("/home/phil/twitter_keys.config")

    # get the OAuth keys
    consumer_key = config.get('Keys', 'consumer_key')
    consumer_secret = config.get('Keys', 'consumer_secret')
    access_token = config.get('Keys', 'access_token')
    access_token_secret = config.get('Keys', 'access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)

def getTweetsFromUser(api, username):
    tweetsString = ""
    last_id = None
    while True:
        # twitter only allows you to fetch 200 tweets per request
        tweets = api.user_timeline(screen_name = username, count = 200, max_id = last_id)
        if not tweets:
            break
        # append the current tweets to tweetsString; keep track of the end of 
        # the tweet so that individual tweets can be retrieved from the text
        # corpus later
        tweetsString = "".join((tweetsString, "".join([" ".join([tweet.text.encode('ascii', 'ignore').lower(), "ENDTWEET\n"]) for tweet in tweets])))
        last_id = tweet.id - 1
    return tweetsString
