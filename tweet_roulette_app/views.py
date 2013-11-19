from django.core import serializers
from django.core.cache import cache
from django.db.models import F
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from django.utils import simplejson
from models import TwitterAccount
from tweepy import TweepError
from utils import twitter
from utils.nlp import CorpusCache, NLPCorpus

#need to instantiate this object only once
TWITTER_API = twitter.getAPI()

def tweet_roulette_form(request):
    return render(request, 'tweet_roulette.html')
    
def create_account(request):
    if request.method == 'POST':
        name = request.POST['username']
        try:
            account = TwitterAccount.objects.get(username=name)
        except TwitterAccount.DoesNotExist:
            try:
                corpus = twitter.getTweetsFromUser(TWITTER_API, name)
                if corpus:
                    account = TwitterAccount(username=name, text_corpus=corpus, num_queries=0)
                    account.save()
                else:
                    return render(request, 'tweet_roulette.html', {'error' : "@" + name + " hasn't tweeted anything yet. Try again with another account",})  
            except TweepError, e:
                # the error code for a non-existent username is 34
                if "34" in str(e):
                    error = 'Username "' + name + '" does not exist. Try again with another username.'
                else:
                    error = str(e)    
                return render(request, 'tweet_roulette.html', {'error' : error,})  
        return redirect('/account/' + name + '/')
    if request.method == 'GET':
        accounts = simplejson.dumps(list(TwitterAccount.objects.order_by('-num_queries').values_list('username', flat=True)))
        return HttpResponse(accounts, mimetype='application/json')

def account(request, account_id):
    try:
        account = TwitterAccount.objects.get(username=account_id)
        # increment num_queries to keep track of popularity of accounts
        account.num_queries = F('num_queries') + 1
        account.save()
        nlp_corpus = cache.get(account.username)
        if not nlp_corpus:
            nlp_corpus = NLPCorpus(account.text_corpus, "[@#$]?\w+(['-_:/.]+\w+)*", "ENDTWEET", 2, 120)
            cache.set(account.username, nlp_corpus)
        tweet = nlp_corpus.generate_sentence()
        return render(request, 'account.html', {'username' : account_id, 'tweet': tweet,})
    except TwitterAccount.DoesNotExist:
        raise Http404
