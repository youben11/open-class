from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .models import *
from .forms import *


def index(request):
    return render(request, "openclass/home.html")

def workshops_list(request):
    w = Workshop.objects.all()
    return render(request, "openclass/listworkshop.html", {"list":w})

def workshops_detail(request, pk):
    return render(request, "openclass/workshop.html")

def members_list(request):
    return HttpResponse('members_list')

def members_detail(request, pk):
    return HttpResponse('members_detail')

def badges_list(request):
    return HttpResponse('badges_list')

@login_required()
def profile(request):
    return render(request, "openclass/profile.html")

def prefs(request):
    user = request.user
    age = user.profile.get_age
    return render(request, "openclass/user-preferences.html", {"age":age})

def signup(request):

    tags = Tag.objects.all()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.score = 0
            profile.save()
            #should verify the user via email
            login(request, user)
            return redirect('/profile')

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context = {"user_form":user_form, "user_profile_form":user_profile_form}
    return render(request, 'openclass/signup.html', context)


def submit_workshop(request):
    if request.method == "POST":
        workshop_form = WorkshopForm(request.POST)
        if workshop_form.is_valid():
            workshop_form.save()
            return HttpResponse("Thanks, Your workshop has been submitted")

    else:
        workshop_form = WorkshopForm()

    context = {"workshop_form": workshop_form}
    return render(request, "openclass/submit_workshop.html", context)


def moderation(request):
    return render(request, "openclass/moderation.html")

def user_settings(request):
    settings_form = UserSettings(request.POST, instance=request.user)
    if request.method == "POST":
        if settings_form.is_valid():
            user = settings_form.save(commit=False)
            user.save()
            return HttpResponse("Thanks, Your workshop has been submitted")
    context = {"user_settings":settings_form}
    return render(request, "openclass/user-settings.html", context)