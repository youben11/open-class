from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *

def index(request):
    return HttpResponse('Hello, Welcome to OpenClass')

def workshops_list(request):
    w = Workshop.objects.all()
    return render(request, "openclass/listworkshop.html", {"list":w})

def workshops_detail(request, pk):
    return HttpResponse('workshops_detail')

def members_list(request):
    return HttpResponse('members_list')

def members_detail(request, pk):
    return HttpResponse('members_detail')

def badges_list(request):
    return HttpResponse('badges_list')

def profile(request):
    user = request.user
    w = Workshop.objects.all()
    return render(request, "openclass/profile.html", {"w":w})

def signup(request):

    tags = Tag.objects.all()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            return HttpResponse("everything valid")

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context = {"user_form":user_form, "user_profile_form":user_profile_form}
    return render(request, 'openclass/signup.html', context)
    