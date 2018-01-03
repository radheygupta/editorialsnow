from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from editorials.models import Editorials
from .forms import RegistrationForm, LoginForm, UserForm, ProfileForm
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction


def index(request, page=1):
    latest_edi_list = Editorials.objects.filter().order_by('-published_date')
    paginator = Paginator(latest_edi_list, 10)

    try:
        editorialsList = paginator.page(page)
    except PageNotAnInteger:
        editorialsList = paginator.page(1)  # show first page if page is not PageNotAnInteger
    except EmptyPage:
        editorialsList = paginator.page(paginator.num_pages)

    startPoint = 1
    endPoint = editorialsList.paginator.num_pages

    if editorialsList.paginator.num_pages > 10:
        if editorialsList.number < 6:
            startPoint = 1
            endPoint = 10
        elif editorialsList.number + 4 >= editorialsList.paginator.num_pages:
            startPoint = editorialsList.paginator.num_pages - 9
            endPoint = editorialsList.paginator.num_pages
        else:
            startPoint = editorialsList.number - 5
            endPoint = editorialsList.number + 4

    pageList = range(startPoint, endPoint + 1)

    return render(request, 'editorials/index.html', {'latest_edi_list': editorialsList, 'pageList': pageList})


def display(request, edt_id, slug=None):
    edtObj = Editorials.objects.get(pk=edt_id)
    if slug != edtObj.slug:
        if edtObj.slug is not None:
            uri = '/editorials/show/' + edt_id + '/' + edtObj.slug + '/'
        else:
            uri = '/editorials/show/' + edt_id + '/'
        return HttpResponsePermanentRedirect(uri)
    return render(request, 'editorials/display.html', {'edtObj': edtObj})


def ajaxsignup(request):
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
                response_data['data'] = {'password': 'Email or Password is incoorrect.'}
        else:
            response_data['result'] = 'error'
            response_data['data'] = form.errors
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def userlogin(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        # form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # User.objects.all().filter()
            print("{}:{}".format(username, password))
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("User logged in : {}".format(user.username))
                return redirect('/editorials/')
    print("User login failed")
    return render(request, 'editorials/login.html', {'login_form': form})


def userregistration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/editorials/')
    return render(request, 'editorials/register.html', {'register_form': form})


def userlogout(request):
    logout(request)
    return redirect('/editorials/')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('/editorials/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'editorials/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
