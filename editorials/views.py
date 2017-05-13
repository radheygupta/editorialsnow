# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.template import loader
# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from editorials.models import Editorials

def index(request,page=1):
    latest_edi_list = Editorials.objects.filter().order_by('-published_date')
    paginator = Paginator(latest_edi_list, 10)
       
    try:
        editorialsList = paginator.page(page)
    except PageNotAnInteger:
        editorialsList = paginator.page(1) # show first page if page is not PageNotAnInteger
    except EmptyPage:
        editorialsList = paginator.page(paginator.num_pages)
    
    startPoint = 1
    endPoint = editorialsList.paginator.num_pages
   
    if(editorialsList.paginator.num_pages > 10):          
        if( editorialsList.number < 6 ):
            startPoint = 1
            endPoint = 10
        elif( editorialsList.number+4 >= editorialsList.paginator.num_pages ):
            startPoint = editorialsList.paginator.num_pages-9
            endPoint = editorialsList.paginator.num_pages
        else:
            startPoint = editorialsList.number-5 
            endPoint = editorialsList.number+4
               
    pageList = range(startPoint,endPoint+1)
        
    return render(request, 'editorials/index.html', {'latest_edi_list': editorialsList,'pageList':pageList })
   
def display(request,edt_id):
    edtObj = Editorials.objects.get(pk=edt_id)
    return render(request, 'editorials/display.html', {'edtObj': edtObj})
