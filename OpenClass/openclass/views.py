from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.forms.models import model_to_dict
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from .models import *
from .forms import *
from . import email
import datetime

def index(request):
    return render(request, "openclass/home.html")

def moderation(request):
    menu_item = "dashboard"
    submitted_workshops = Workshop.objects.filter(status=Workshop.PENDING)
    accepted_workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    refused_workshops = Workshop.objects.filter(status=Workshop.REFUSED)
    done_workshops = Workshop.objects.filter(status=Workshop.DONE)
    workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    context = { "workshops":workshops,
                "submitted_workshops":submitted_workshops,
                "accepted_workshops":accepted_workshops,
                "refused_workshops":refused_workshops,
                "done_workshops":done_workshops,
                "menu_item":menu_item
              }
    return render(
                request,
                "openclass/moderation_dashboard.html",
                context
                )

#moderator
def moderation_submitted_workshops(request):
    menu_item = "submitted_workshops"
    pending_workshops = Workshop.objects.filter(status=Workshop.PENDING)
    date_now = timezone.now()
    context = {'submissions': pending_workshops, 'date_now': date_now, 'menu_item': menu_item}
    return render(request, 'openclass/moderation_submitted-workshops.html', context)

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
    if request.is_ajax():
        tag_method = request.POST['filter']
        if tag_method == 'TAG':
            tag_filtere = request.POST['tag']
            tag = Tag.objects.get(name=tag_filtere)
            workshop_list = Workshop.objects.filter(topics=tag.id)
            context = {'workshop_list': workshop_list}
            return render(request, "openclass/listworkshop_item.html", context)

        elif tag_method == 'TIME':
            time_filter = request.POST['time']
            today = datetime.datetime.today()
            this_week = today + datetime.timedelta(6)
            tomorrow = today + datetime.timedelta(1)
            if time_filter == 'Tomorrow':
                workshop_list = Workshop.objects.filter(start_date__date = tomorrow.date())

            elif time_filter == 'This week':
                workshop_list = Workshop.objects.filter(start_date__lte = this_week.date(),start_date__gte = today.date())

            elif time_filter == 'Next week':
                next_week = this_week + datetime.timedelta(6)
                workshop_list = Workshop.objects.filter(start_date__lte = next_week.date(),start_date__gte = this_week.date())

            elif time_filter == 'This month':
                workshop_list = Workshop.objects.filter(start_date__month = today.month,start_date__year = today.year)

            context = {'workshop_list': workshop_list}
            return render(request,"openclass/listworkshop_item.html",context)
    else :
        workshops = Workshop.objects.filter(Q(status=Workshop.ACCEPTED) | Q(status=Workshop.DONE)
        )
        tags = Tag.objects.all()
        return render(request, "openclass/listworkshop.html", {"workshop_list":workshops, "tags":tags})

def upcoming_workshops_list(request):
    workshops = Workshop.objects.filter(
                                    start_date__gte = datetime.datetime.now(),
                                    status=Workshop.ACCEPTED,
                                    )
    return render(request, "openclass/listworkshop.html", {"workshop_list":workshops})

def workshops_detail(request, workshop_pk):
    workshop = get_object_or_404(
                        Workshop,
                        Q(status=Workshop.ACCEPTED) | Q(status=Workshop.DONE),
                        pk=workshop_pk,
                        )
    context = {'workshop': workshop}
    if request.user.is_authenticated:
        context['is_registered'] = request.user.profile.is_registered(workshop)
        if context['is_registered']:
            context.update(workshop.check_registration(request.user.profile))

    return render(request, "openclass/workshop.html",context)

def workshops_filter_tag(request):
    tag_filtered = request.POST['tag']
    tag= Tag.objects.get(name=tag_filtered)
    workshop_list = list(Workshop.objects.filter(topics=tag.id).values())
    result = {'data': workshop_list}
    return render(request,"openclass/listworkshop_item.html",result)

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
    preference = request.user.profile.preference
    if request.method == 'POST':
        user_prefs_form = UserPrefsForm(request.POST, instance=preference)
        if user_prefs_form.is_valid():
            user_prefs_form.save()
    else:
        user_prefs_form = UserPrefsForm(instance=preference)
    context = {'user_prefs_form': user_prefs_form}
    return render(request, "openclass/user-preferences.html", context)

@transaction.atomic
def signup(request):
    tags = Tag.objects.all()

    if request.user.is_authenticated:
        return redirect(reverse('openclass:profile'))

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile.preference = Preference.objects.create(profile=profile)
            profile_form.save_m2m()
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
        profile_form = ProfileForm()

    context = {"user_form":user_form, "profile_form":profile_form}
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



@login_required()
def user_settings(request):
    if request.method == "POST":
        user_settings_form = UserSettingsForm(request.POST, instance=request.user)
        profile_settings_form = ProfileSettingsFrom(request.POST, request.FILES, instance=request.user.profile)
        if user_settings_form.is_valid():
            user_settings_form.save()
        if profile_settings_form.is_valid():
            profile_settings_form.save()
    else:
        user_settings_form = UserSettingsForm(instance=request.user)
        profile_settings_form = ProfileSettingsFrom(instance=request.user.profile)

    context = {"user_settings_form": user_settings_form, "profile_settings_form": profile_settings_form}
    return render(request, "openclass/user-settings.html", context)

#TODO only moderator
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
        if registration.present:
            registration.absent()
        else:
            registration.confirm_presence()

        kwargs = {'workshop_pk': workshop_pk}
        return redirect(reverse('openclass:attendance', kwargs=kwargs))

    context = {"registration": registration, "workshop":workshop, "profile":profile}
    return render(request, "openclass/user-attendance.html", context)

@login_required()
def register_to_workshop(request):
    workshop_pk = request.POST['workshop_pk']
    # TODO : register only to accepted workshops
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
    #TODO can't cancel a registration for a DONE workshop
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
    start_date = workshop.start_date
    end_date = start_date + workshop.duration

    # check if the workshop is already done
    if workshop.status == Workshop.DONE:
        context = {"is_done": True}
        return render(request, "openclass/ask_question.html", context)

    # check if the workshop is accepted
    # must check DONE status before this check
    # (status == DONE) => (status != ACCEPTED)
    if workshop.status != Workshop.ACCEPTED:
        context = {"not_accepted": True}
        return render(request, "openclass/ask_question.html", context)

    # check if the workshop already started
    if timezone.now() < start_date:
        context = {"not_started": True}
        return render(request, "openclass/ask_question.html", context)

    registration = request.user.profile.get_workshop_registration(workshop)
    # check if the member is registered to the workshop
    if registration is None:
        context = {"not_registered": True}
        return render(request, "openclass/ask_question.html", context)

    # check if the member is present
    if not registration.present:
        context = {"not_present": True}
        return render(request, "openclass/ask_question.html", context)

    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user.profile
            question.workshop = workshop
            question.save()
            kwargs = {"workshop_pk":workshop_pk}
            return redirect(reverse('openclass:workshops_detail',kwargs=kwargs))

    else:
        question_form = QuestionForm()

    context = {"question_form": question_form}
    return render(request, "openclass/ask_question.html", context)


@login_required()
def workshop_questions_list(request, workshop_pk):
    workshop = get_object_or_404(Workshop, pk=workshop_pk)
    questions_list = Question.objects.filter(workshop=workshop)
    context = {"questions_list": questions_list}

    # only the animator have permission to see the asked questions
    if workshop.animator != request.user.profile:
        context["permission_denied"] = True
        return render(request, "openclass/workshop_questions_list.html", context)

    # if it's an ajax GET request return the questions_list only
    if request.is_ajax():
        return render(request, "openclass/questions_list.html", context)
    # if it's a normal GET return the hole page
    else:
        return render(request, "openclass/workshop_questions_list.html", context)


def faq(request):
    faqs = FAQ.objects.all()
    context = {'faqs': faqs}
    return render(request, "openclass/faq.html", context)

@login_required
def feedback(request, workshop_pk):
    workshop = get_object_or_404(
                        Workshop,
                        Q(status=Workshop.ACCEPTED) | Q(status=Workshop.DONE),
                        pk=workshop_pk
                        )
    profile = request.user.profile
    context = {}
    if timezone.now() < workshop.end_date():
        title = "Openclass - Feedback"
        msg = 'Attendees can submit their feedback after the completion of the workshop'
        context = {'title': title, 'msg': msg}
        return render(request, 'openclass/info.html', context)
    try:
        registration = Registration.objects.get(
                                        workshop=workshop,
                                        profile=profile
                                        )
        if not registration.present:
            title = "Openclass - Feedback"
            msg = 'Only attendees can submit a feedback'
            context = {'title': title, 'msg': msg}
            return render(request, 'openclass/info.html', context)
    except:
        title = "Openclass - Feedback"
        msg = 'You are not registred to this workshop'
        context = {'title': title, 'msg': msg}
        return render(request, 'openclass/info.html', context)
    try:
        feedback = Feedback.objects.get(workshop=workshop, author=profile)
        context['is_feedbacked'] = True
    except Feedback.DoesNotExist:
        context['is_feedbacked'] = False

    if context['is_feedbacked']:
        return render(request, "openclass/feedback.html", context)

    mc_questions_prefix = "mc_question_"
    context['mc_questions_prefix'] = mc_questions_prefix
    if request.method == "GET":
        mc_questions = workshop.mc_questions.all()
        context['questions'] = mc_questions
        return render(request, "openclass/feedback.html", context)

    elif request.method == "POST":
        mc_questions_re = "^%s\d+$" % mc_questions_prefix
        comment = request.POST['comment']
        feedback = Feedback.objects.create(
                        workshop=workshop,
                        author=profile,
                        submission_date=timezone.now(),
                        comment=comment
                        )
        for mc_question_pk, choice_pk in request.POST.items():
            if re.match(mc_questions_re, mc_question_pk):
                mc_question_pk = mc_question_pk.split('_')[-1]
                try:
                    mc_question = MCQuestion.objects.get(pk=mc_question_pk)
                    if workshop not in mc_question.workshop_set.all():
                        continue
                    choice = Choice.objects.get(pk=choice_pk)
                    if choice not in mc_question.choices.all():
                        continue
                except:
                    pass
                feedback.choices.add(choice_pk)
        title = 'Feedback submitted'
        msg = 'Thank you, your feedback has been submitted'
        context = {'title': title, 'msg': msg}
        return render(request, 'openclass/info.html', context)
