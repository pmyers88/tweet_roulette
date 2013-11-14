from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from models import TwitterAccount
from tweepy import TweepError
from utils import twitter


def home(request):
    return HttpResponse('HELLO WORLD!')

def tweet_roulette_form(request):
    return render(request, 'tweet_roulette.html')
    
def create_account(request):
    if request.method == 'POST':
        name = request.POST['username']
        print name
        try:
            account = TwitterAccount.objects.get(username=name)
        except TwitterAccount.DoesNotExist:
            try:
                account = TwitterAccount(username=name, textCorpus=twitter.getTweetsFromUser(name))
                account.save()
            except TweepError, e:
                # the error code for a non-existent username is 34
                if "34" in str(e):
                    error = 'Username "' + name + '" does not exist. Try again with another username.'
                else:
                    error = str(e)    
                return render(request, 'tweet_roulette.html', {'error' : error,})  
        return redirect('/account/' + name + '/')
    return redirect('/')

def account(request, account_id):
    try:
        account = TwitterAccount.objects.get(username=account_id)
    except TwitterAccount.DoesNotExist:
        raise Http404
    return render(request, 'account.html', {'username' : account_id, 'tweet': account.generateTweet(2),})