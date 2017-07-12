# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate, login, logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from editorials.models import Editorials
from .forms import RegistrationForm, LoginForm
import json

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

def ajaxsignup(request):
    #email = request.POST.get(email,None)
    #data = {
        #'ErrorMsg': Users.objects.filter(email__iexact=email).exists()
    #}
    if request.method == 'POST' and request.is_ajax() is True:
        form = RegistrationForm(request.POST)
        response_data = {}
        if form.is_valid():
            user = form.save()
            response_data['result'] = 'success'
            login(request, user)
        else:
            response_data['result'] = 'error'
            response_data['data'] = form.errors
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def ajaxlogin(request):
    if request.method == 'POST' and request.is_ajax() is True:
        form = LoginForm(request.POST)
        response_data = {}
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response_data['result'] = 'success'
            else:
                response_data['result'] = 'error'
                response_data['data'] = {'password':'Email or Password is incoorrect.'}
        else:
            response_data['result'] = 'error'
            response_data['data'] = form.errors
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
def userlogout(request):
    logout(request)
    return redirect('/editorials/')
