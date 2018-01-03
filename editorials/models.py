# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Editorials(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=500, null=True, blank=True)
    content = models.CharField(max_length=8000)
    author = models.CharField(max_length=50, null=True, blank=True)
    news_paper = models.CharField(max_length=50)
    published_date = models.DateTimeField()
    fetched_date = models.DateTimeField(auto_now_add=True)
    fetched_url = models.URLField(max_length=400)
    # slug = models.CharField(max_length=120)
    
    class Meta:
        db_table = 'editorials'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(null=True, blank=True, max_length=200)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

