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
    return HttpResponse('workshops_detail')

def members_list(request):
    return HttpResponse('members_list')

def members_detail(request, pk):
    return HttpResponse('members_detail')

def badges_list(request):
    return HttpResponse('badges_list')

@login_required(login_url='/login')
def profile(request):
    user = request.user
    w_at = user.profile.workshops_attended()
    w_an = user.profile.workshops_animated()
    age = user.profile.get_age
    return render(request, "openclass/profile.html", {"w_at":w_at,"w_an":w_an,"age":age})

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
