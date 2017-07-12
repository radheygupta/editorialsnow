# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Editorials(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=500,null=True,blank=True)
    content = models.CharField(max_length=8000)
    author = models.CharField(max_length=50,null=True,blank=True)
    news_paper = models.CharField(max_length=50)
    published_date = models.DateTimeField()
    fetched_date = models.DateTimeField(auto_now_add=True)
    fetched_url = models.URLField(max_length=400)
    
    class Meta:
        db_table = 'editorials'

    
