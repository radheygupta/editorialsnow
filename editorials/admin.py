# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from .models import Editorials

class EditorialsModelForm(forms.ModelForm):
    class Meta:
        model = Editorials
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'subtitle': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
        
class EditorialsAdmin( admin.ModelAdmin ):
    form = EditorialsModelForm
    list_display = ('title', 'published_date', 'news_paper')
    list_filter = ['published_date']
    search_fields = ['title']


admin.site.register(Editorials, EditorialsAdmin)
