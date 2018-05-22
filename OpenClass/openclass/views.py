from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.forms.models import model_to_dict
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from .models import *
from .forms import *
from . import email


def index(request):
    return render(request, "openclass/home.html")

#moderator
def moderation_submitted_workshops(request):
    pending_workshops = Workshop.objects.filter(status=Workshop.PENDING)
    date_now = timezone.now()
    context = {'submissions': pending_workshops, 'date_now': date_now}
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
    tags = Tag.objects.all()
    return render(request, "openclass/listworkshop.html", {"workshops":workshops,"tags":tags})

def upcoming_workshops_list(request):
    workshops = Workshop.objects.filter(
                                    start_date__gte=datetime.now(),
                                    status=Workshop.ACCEPTED,
                                    )
    return render(request, "openclass/listworkshop.html", {"workshops":workshops})

def workshops_detail(request, workshop_pk):
    workshop = get_object_or_404(
                        Workshop,
                        pk=workshop_pk,
                        status=Workshop.ACCEPTED,
                        )
    context = {'workshop': workshop}
    if request.user.is_authenticated:
        context['is_registered'] = request.user.profile.is_registered(workshop)
        if context['is_registered']:
            context.update(workshop.check_registration(request.user.profile))
            is_canceled = context['is_canceled']

    return render(request, "openclass/workshop.html",context)

def workshops_filter_tag(request):
    tag_filtered = request.POST['tag']
    tag= Tag.objects.get(name=tag_filtered)
    workshop_list = list(Workshop.objects.filter(topics=tag.id).values())
    result = {'data': workshop_list}
    return JsonResponse(result)


@login_required()
def members_list(request):
	users = User.objects.filter()
	return render(request, "openclass/member_list.html", {"users":users})

@login_required()
def members_detail(request, username):
    user = User.objects.get(username = username)
    return render(request, "openclass/profile.html", {"user":user})

def badges_list(request):
    badges = Badge.objects.all()
    context = {"badges": badges}
    return render(request, "openclass/badges.html", context)

@login_required()
def profile(request):
    return render(request, "openclass/profile.html")

@login_required()
def prefs(request):
    return render(request, "openclass/user-preferences.html")

@transaction.atomic
def signup(request):
    tags = Tag.objects.all()

    if request.user.is_authenticated:
        return redirect(reverse('openclass:profile'))

    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user.save()
            if settings.EMAIL_VERIFICATION:
                user.is_active = False
                user.save()
                token = profile.generate_verification_token()
                email.send_verification_mail(user, token)
                return HttpResponse(token)
            else:
                login(request, user)
                return redirect(reverse('openclass:profile'))

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()

    context = {"user_form":user_form, "user_profile_form":user_profile_form}
    return render(request, 'openclass/signup.html', context)

def verify(request, token):
    try:
        verification_token = VerificationToken.objects.get(value=token)
    except VerificationToken.DoesNotExist:
        return HttpResponse("Bad token")

    user = verification_token.verify(token)
    if user:
        login(request, user)
        return redirect(reverse('openclass:profile'))
    else:
        return HttpResponse("Bad token")

@login_required()
def submit_workshop(request):
    if request.method == "POST":
        workshop_form = WorkshopForm(request.POST, request.FILES)
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
    workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
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
        #?? POST only ??
        registration.present = not registration.present
        registration.save()
        kwargs = {'workshop_pk': workshop_pk}
        return redirect(reverse('openclass:attendance', kwargs=kwargs))

    context = {"registration": registration, "workshop":workshop, "profile":profile}
    return render(request, "openclass/user-attendance.html", context)

@login_required()
def register_to_workshop(request):
    workshop_pk = request.POST['workshop_pk']

    try:
        workshop = Workshop.objects.get(pk=workshop_pk)
    except Workshop.DoesNotExist:
        error = {'status': 'workshop_does_not_exist'}
        return JsonResponse(error)

    if request.user.profile.is_registered(workshop):
        error = {'status': 'already_registred'}
        return JsonResponse(error)

    if not workshop.is_registration_open():
        response = {'status': 'registration_closed'}
        return JsonResponse(response)

    if workshop.register(request.user.profile):
        response = {'status': 'registered'}
    else:
        response = {'statuts': "can't register"}

    return JsonResponse(response)

@login_required()
def cancel_registration(request):
    workshop_pk = request.POST['workshop_pk']

    try:
        workshop = Workshop.objects.get(pk=workshop_pk)
    except Workshop.DoesNotExist:
        error = {'status': 'workshop_does_not_exist'}
        return JsonResponse(error)

    if not request.user.profile.is_registered(workshop):
        error = {'status': 'not_registred'}
        return JsonResponse(error)

    if not request.user.profile.can_cancel_registration(workshop):
        response = {'status': "can't cancel"}
        return JsonResponse(response)

    if workshop.cancel_registration(request.user.profile):
        response = {'status': 'canceled'}
    else:
        response = {'status': "can't cancel"}

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
