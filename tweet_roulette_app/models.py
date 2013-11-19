from django.db import models
from utils.nlp import NLPCorpus

class BlobField(models.Field):
    description = "MediumBlob"
    def db_type(self, connection):
        return 'mediumblob'

class TwitterAccount(models.Model):
    username = models.CharField(max_length=15, unique=True)
    text_corpus = BlobField()
    num_queries = models.IntegerField()
    last_updated = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'Username: %s; Last Updated: %s'  % (self.username, self.last_updated)