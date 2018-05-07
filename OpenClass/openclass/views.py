from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    return HttpResponse('Hello, Welcome to OpenClass')

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

@login_required(login_url='/login')
def profile(request):
    user = request.user
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

