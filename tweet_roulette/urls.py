from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'tweet_roulette_app.views.tweet_roulette_form'),
     url(r'^account/$', 'tweet_roulette_app.views.create_account'),
     url(r'^account/(?P<account_id>\w{1,15})/$', 'tweet_roulette_app.views.account'),
     
     # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
