from django.http import HttpResponse
from django.shortcuts import render
from .models import Workshop

def index(request):
    return HttpResponse('Hello, Welcome to OpenClass')

def workshops_list(request):
    return HttpResponse('workshops_list')

def workshops_detail(request, pk):
    return HttpResponse('workshops_detail')

def members_list(request):
    return HttpResponse('members_list')

def members_detail(request, pk):
    return HttpResponse('members_detail')

def badges_list(request):
    return HttpResponse('badges_list')

def profile(request):
   w = Workshop.objects.all()
   return render(request, "profile.html", {"w":w})