from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.forms.models import model_to_dict
from django.urls import reverse
from .models import *
from .forms import *


def index(request):
    return render(request, "openclass/home.html")

#moderator
def moderation_submitted_workshops(request):
    pending_workshops = Workshop.objects.filter(status=Workshop.PENDING)
    context = {'submissions': pending_workshops}
    return render(request, 'openclass/submitted-workshops.html', context)

#moderator
def moderation_submitted_workshops_decision(request):
    ACCEPT = "accept"
    REFUSE = "refuse"
    workshop_pk = request.POST['workshop_pk']
    decision = request.POST['decision']

    try:
        workshop = Workshop.objects.get(pk=workshop_pk)
    except Workshop.DoesNotExist:
        error = {'status': 'workshop_does_not_exist'}
        return JsonResponse(error)

    if decision == ACCEPT:
        if workshop.accept():
            response = {'status': 'accepted'}
        else:
            response = {'status': "can't accept"}

    elif decision == REFUSE:
        if workshop.refuse():
            response = {'status': 'refused'}
        else:
            response = {'status': "can't refuse"}
    else:
        response = {'status': 'invalid decision'}

    return JsonResponse(response)


def workshops_list(request):
    workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    return render(request, "openclass/listworkshop.html", {"workshops":workshops})

def upcoming_workshops_list(request):
    workshops = Workshop.objects.filter(
                                    start_date__gte=datetime.now(),
                                    status=Workshop.ACCEPTED,
                                    )
    return render(request, "openclass/listworkshop.html", {"workshops":workshops})

def workshops_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop,pk=workshop_id)
    is_registered = workshop.check_registration(request.user.profile)
    return render(request, "openclass/workshop.html",{"workshop":workshop, "is_registered":is_registered})

def members_list(request):
	profiles = Profile.objects.all()
	return render(request, "openclass/member_list.html", {"profiles":profiles})


def members_detail(request, username):
    user = User.objects.get(username = username)
    return render(request, "openclass/profile.html", {"user":user})

def badges_list(request):
    return HttpResponse('badges_list')

@login_required()
def profile(request):
    user = request.user
    return render(request, "openclass/profile.html")

def prefs(request):
    user = request.user
    age = user.profile.get_age
    return render(request, "openclass/user-preferences.html", {"age":age})

def signup(request):

    tags = Tag.objects.all()

    if request.user.is_authenticated:
        return redirect('/profile')

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

@login_required()
def submit_workshop(request):
    if request.method == "POST":
        workshop_form = WorkshopForm(request.POST)
        if workshop_form.is_valid():
            workshop = workshop_form.save(commit=False)
            workshop.submission_date = datetime.now()
            workshop.status = Workshop.PENDING
            workshop.animator = request.user.profile
            workshop.save()
            return HttpResponse("Thanks, Your workshop has been submitted")

    else:
        workshop_form = WorkshopForm()

    context = {"workshop_form": workshop_form}
    return render(request, "openclass/submit_workshop.html", context)


def moderation(request):
    workshops = Workshop.objects.all()
    return render(request, "openclass/moderation.html", {"workshops":workshops})

@login_required()
def user_settings(request):
    if request.method == "POST":
        settings_form = UserSettings(request.POST, instance=request.user)
        if settings_form.is_valid():
            user = settings_form.save()
    else:
        settings_form = UserSettings(initial=model_to_dict(request.user))

    context = {"user_settings":settings_form}
    return render(request, "openclass/user-settings.html", context)

def attendance(request,workshop_pk):
    workshop = get_object_or_404(Workshop, pk = workshop_pk)
    registrations = Registration.objects.all().filter(workshop=workshop)
    context = {"registrations": registrations,"workshop":workshop}
    return render(request, "openclass/attendance.html", context)

def user_attendance(request, workshop_pk, user_pk):
    workshop = get_object_or_404(Workshop, pk = workshop_pk)
    profile = get_object_or_404(Profile, id = user_pk)
    registration = Registration.objects.get(workshop=workshop,profile=profile)
    if request.method=="POST":
        registration.present = not registration.present
        registration.save()
        return redirect('/attendance/'+str(workshop_pk))

    context = {"registration": registration, "workshop":workshop, "profile":profile}
    return render(request, "openclass/user-attendance.html", context)

@login_required()
def register_to_workshop(request):
    workshop_pk = request.POST['workshop_pk']
    # add checks
    try:
        workshop = Workshop.objects.get(pk=workshop_pk)
    except Workshop.DoesNotExist:
        error = {'status': 'workshop_does_not_exist'}
        return JsonResponse(error)

    registration = Registration()
    registration.workshop = workshop
    registration.profile = request.user.profile
    registration.status = Registration.PENDING
    registration.save()

    response = {'status': 'registred'}
    return JsonResponse(response)

def user_registrations(request):
    registrations = request.user.profile.get_registrations
    return render(request, "openclass/user-registrations.html", {"registrations":registrations})


@login_required()
def ask_question(request, workshop_pk):
    workshop = get_object_or_404(Workshop, pk=workshop_pk)
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form .is_valid():
            question = question_form .save(commit=False)
            question.author = request.user.profile
            question.workshop = workshop
            question.save()
            return HttpResponse("Thanks, Your Question has been submitted")

    else:
        question_form = QuestionForm()

    context = {"question_form": question_form}
    return render(request, "openclass/ask_question.html", context)
