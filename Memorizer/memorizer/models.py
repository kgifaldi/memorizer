from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.



class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    numMemorized = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    toMemorize = {}
    nextReview = {}
    def __str__(self):
        return self.username
