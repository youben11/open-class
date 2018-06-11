from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.forms.models import model_to_dict
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from .models import *
from .forms import *
from . import email
import datetime

def is_moderator(user):
    return user.is_staff

def index(request):
    return render(request, "openclass/home.html")

def about(request):
    return render(request, "openclass/about.html")
@login_required
@user_passes_test(is_moderator)
def moderation(request):
    menu_item = "dashboard"
    submitted_workshops = Workshop.objects.filter(status=Workshop.PENDING)
    accepted_workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    refused_workshops = Workshop.objects.filter(status=Workshop.REFUSED)
    done_workshops = Workshop.objects.filter(status=Workshop.DONE)
    workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    users = User.objects.all().order_by('-date_joined')[:4]
    context = {
                "workshops":workshops,
                "submitted_workshops":submitted_workshops,
                "accepted_workshops":accepted_workshops,
                "refused_workshops":refused_workshops,
                "done_workshops":done_workshops,
                "menu_item":menu_item,
                "users":users
              }
    return render(
                request,
                "openclass/moderation_dashboard.html",
                context
                )

@login_required
@user_passes_test(is_moderator)
def moderation_workshops(request):
    table_title = "All Workshops"
    menu_item = "workshops"
    workshops = Workshop.objects.all()
    workshops = workshops.prefetch_related(
                                                        'animator',
                                                        'animator__user'
                                                        )
    date_now = timezone.now()
    context = {
                'workshops': workshops,
                'date_now': date_now,
                'menu_item': menu_item,
                'table_title': table_title
              }

    return render(request, 'openclass/moderation_workshops.html', context)

@login_required
@user_passes_test(is_moderator)
def moderation_attendance(request):
    table_title = "Manage Attendance"
    menu_item = "attendance"
    accepted_workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    accepted_workshops = accepted_workshops.prefetch_related(
                                                        'animator',
                                                        'animator__user'
                                                        )
    date_now = timezone.now()
    context = {
                'accepted_workshops': accepted_workshops,
                'date_now': date_now,
                'menu_item': menu_item,
                'table_title': table_title
              }

    return render(request, 'openclass/moderation_attendance.html', context)

@login_required
@user_passes_test(is_moderator)
def moderation_workshop_attendance(request,workshop_pk):
    workshop = get_object_or_404(Workshop, pk = workshop_pk)
    registrations = Registration.objects.all().filter(workshop=workshop)
    date_now = timezone.now()
    context = {"registrations": registrations,"workshop":workshop, "date_now": date_now}
    return render(request, "openclass/attendance.html", context)

@login_required
@user_passes_test(is_moderator)
def moderation_workshop_user_attendance(request, workshop_pk, user_pk):
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
        return redirect(reverse('openclass:moderation_workshop_attendance', kwargs=kwargs))

    context = {"registration": registration, "workshop":workshop, "profile":profile}
    return render(request, "openclass/user-attendance.html", context)

@login_required
@user_passes_test(is_moderator)
def moderation_accepted_workshops(request):
    menu_item = "accepted_workshops"
    accepted_workshops = Workshop.objects.filter(status=Workshop.ACCEPTED)
    accepted_workshops = accepted_workshops.prefetch_related(
                                                        'animator',
                                                        'animator__user'
                                                        )
    date_now = timezone.now()
    context = {
                'accepted_workshops': accepted_workshops,
                'date_now': date_now,
                'menu_item': menu_item
              }
    if request.is_ajax():
        return render(request, "openclass/moderation_accepted-workshops_table.html", context)
    return render(request, 'openclass/moderation_accepted-workshops.html', context)

@login_required
@user_passes_test(is_moderator)
def moderation_done_workshops(request):
    menu_item = "done_workshops"
    done_workshops = Workshop.objects.filter(status=Workshop.DONE)
    done_workshops = done_workshops.prefetch_related(
                                                        'animator',
                                                        'animator__user'
                                                        )
    date_now = timezone.now()
    context = {
                'done_workshops': done_workshops,
                'date_now': date_now,
                'menu_item': menu_item
              }
    return render(request, 'openclass/moderation_done-workshops.html', context)

@login_required
@user_passes_test(is_moderator)
def moderation_submitted_workshops(request):
    menu_item = "submitted_workshops"
    pending_workshops = Workshop.objects.filter(status=Workshop.PENDING)
    pending_workshops = pending_workshops.prefetch_related(
                                                        'animator',
                                                        'animator__user'
                                                        )
    refused_workshops = Workshop.objects.filter(status=Workshop.REFUSED)
    refused_workshops = refused_workshops.prefetch_related(
                                                        'animator',
                                                        'animator__user'
                                                        )
    date_now = timezone.now()
    context = {
                'submissions': pending_workshops,
                'refused_workshops': refused_workshops,
                'date_now': date_now,
                'menu_item': menu_item
              }
    if request.is_ajax():
        return render(request, "openclass/moderation_submitted-workshops_table-accepted.html", context)
    return render(request, 'openclass/moderation_submitted-workshops.html', context)

@login_required
@user_passes_test(is_moderator)
def moderation_submitted_workshops_decision(request):
    ACCEPT = "accept"
    REFUSE = "refuse"
    DONE = "done"

    try:
        workshop_pk = request.POST['workshop_pk']
        decision = request.POST['decision']
    except:
        error = {'status': 'wrong parameters'}
        return JsonResponse(error)

    profile = request.user.profile

    try:
        workshop = Workshop.objects.get(pk=workshop_pk)
    except Workshop.DoesNotExist:
        error = {'status': 'workshop_does_not_exist'}
        return JsonResponse(error)

    if decision == ACCEPT:
        if workshop.accept(profile):
            response = {'status': 'accepted'}
        else:
            response = {'status': "can't accept"}

    elif decision == REFUSE:
        if workshop.refuse(profile):
            response = {'status': 'refused'}
        else:
            response = {'status': "can't refuse"}

    elif decision == DONE:
        if workshop.done():
            response = {'status': 'done'}
        else:
            response = {'status': "can't mark as done"}

    else:
        response = {'status': 'invalid decision'}

    return JsonResponse(response)


def workshops_list(request):
    if request.is_ajax():
        tag_names = list(set(request.POST.getlist('tag[]')))
        time_filters = list(set(request.POST.getlist('time[]')))
        title_filter = request.POST.get('title',"")
        if tag_names or time_filters or title_filter:
            today = timezone.now().date()
            this_week = today + datetime.timedelta(6)
            tomorrow = today + datetime.timedelta(1)
            # filter according to the tag_names
            filters = Q(topics__name__in=tag_names)
            # filter according to the time filters
            if 'Tomorrow' in time_filters:
                filters |= Q(start_date__date=tomorrow)

            if 'This week' in time_filters:
                filters |= Q(
                            start_date__lte=this_week,
                            start_date__gte=today
                            )

            if 'Next week' in time_filters:
                next_week = this_week + datetime.timedelta(6)
                filters |= Q(
                            start_date__lte=next_week,
                            start_date__gte=this_week
                            )

            if 'This month' in time_filters:
                filters |= Q(
                            start_date__month=today.month,
                            start_date__year=today.year
                            )
            if title_filter:
                filters |= Q(title__icontains=title_filter)
            # all filters were ORed to make a final filter
            workshop_list = Workshop.objects.filter(filters).distinct()
            workshop_list = workshop_list.prefetch_related('topics')

            context = {
                        'workshop_list': workshop_list,
                        'times' : time_filters,
                        'tag_names': tag_names
                      }
            return render(request,"openclass/listworkshop_item.html",context)
        else:
            workshops = Workshop.objects.filter(
                                Q(status=Workshop.ACCEPTED) | Q(status=Workshop.DONE)
                                )
            context = {"workshop_list":workshops}
            return render(request, "openclass/listworkshop_item.html", context)

    else :
        workshops = Workshop.objects.filter(
                        Q(status=Workshop.ACCEPTED) | Q(status=Workshop.DONE)
                        ).prefetch_related('topics')
        tags = Tag.objects.all()
        context = {"workshop_list":workshops, "tags":tags}
        return render(request, "openclass/listworkshop.html", context)

def upcoming_workshops_list(request):
    workshops = Workshop.objects.filter(
                                    start_date__gte=timezone.now(),
                                    status=Workshop.ACCEPTED,
                                    ).prefetch_related('topics')
    context = {"workshop_list":workshops}
    return render(request, "openclass/listworkshop.html", context)

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

@login_required
def members_list(request):
    filters = Q(is_active=True, is_superuser=False)
    users = User.objects.filter(filters).prefetch_related('profile')
    return render(request, "openclass/member_list.html", {"users":users})

@login_required
def members_detail(request, username):
    user = get_object_or_404(User, username=username, is_superuser=False)
    return render(request, "openclass/profile.html", {"user":user})

def badges_list(request):
    badges = Badge.objects.all()
    context = {"badges": badges}
    return render(request, "openclass/badges.html", context)

@login_required
def profile(request):
    return render(request, "openclass/profile.html")

@login_required
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
            if settings.EMAIL_ENABLED and settings.EMAIL_VERIFICATION:
                user.is_active = False
                user.save()
                token = profile.generate_verification_token()
                email.send_verification_mail(user, token)
                title = "Confirmation"
                msg = 'Check your inbox to confirm your registration'
                context = {'title': title, 'msg': msg}
                return render(request, 'openclass/info.html', context)
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

@login_required
def submit_workshop(request):
    if request.method == "POST":
        workshop_form = WorkshopForm(request.POST, request.FILES)
        if workshop_form.is_valid():
            workshop = workshop_form.save(commit=False)
            workshop.submission_date = timezone.now()
            workshop.status = Workshop.PENDING
            workshop.animator = request.user.profile
            workshop.save()
            title = "Workshop Submitted"
            msg = 'Thank you, your workshop have been submitted'
            context = {'title': title, 'msg': msg}
            return render(request, 'openclass/info.html', context)

    else:
        workshop_form = WorkshopForm()

    context = {"workshop_form": workshop_form}
    return render(request, "openclass/submit_workshop.html", context)



@login_required
def user_settings(request):
    if request.method == "POST":
        user_settings_form = UserSettingsForm(
                                    request.POST,
                                    instance=request.user
                                    )
        profile_settings_form = ProfileSettingsFrom(
                                    request.POST,
                                    request.FILES,
                                    instance=request.user.profile
                                    )
        if user_settings_form.is_valid():
            user_settings_form.save()
        if profile_settings_form.is_valid():
            profile_settings_form.save()
    else:
        user_settings_form = UserSettingsForm(instance=request.user)
        profile_settings_form = ProfileSettingsFrom(
                                                instance=request.user.profile
                                                )

    context = {
                "user_settings_form": user_settings_form,
                "profile_settings_form": profile_settings_form
              }
    return render(request, "openclass/user-settings.html", context)

@login_required
@user_passes_test(is_moderator)
def attendance(request,workshop_pk):
    workshop = get_object_or_404(Workshop, pk=workshop_pk)
    registrations = Registration.objects.filter(workshop=workshop)
    registrations = registrations.prefetch_related('profile', 'profile__user')
    context = {"registrations": registrations,"workshop":workshop}
    return render(request, "openclass/attendance.html", context)

@login_required
@user_passes_test(is_moderator)
def user_attendance(request, workshop_pk, user_pk):
    workshop = get_object_or_404(Workshop, pk=workshop_pk)
    profile = get_object_or_404(Profile, id=user_pk)
    registration = Registration.objects.get(workshop=workshop,profile=profile)
    if request.method=="POST":
        #?? POST only ??
        if registration.present:
            registration.absent()
        else:
            registration.confirm_presence()

        kwargs = {'workshop_pk': workshop_pk}
        return redirect(reverse('openclass:attendance', kwargs=kwargs))

    context = {
                "registration": registration,
                "workshop":workshop,
                "profile":profile
              }
    return render(request, "openclass/user-attendance.html", context)

@login_required
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

@login_required
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

@login_required
def user_registrations(request):
    registrations = request.user.profile.get_registrations()
    registrations = registrations.prefetch_related('workshop')
    context = {"registrations":registrations}
    return render(request, "openclass/user-registrations.html", context)


@login_required
def ask_question(request, workshop_pk):
    workshop = get_object_or_404(Workshop, pk=workshop_pk)
    start_date = workshop.start_date
    end_date = start_date + workshop.duration

    # check if the workshop is already done
    if workshop.status == Workshop.DONE  or timezone.now() > end_date:
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


@login_required
def workshop_questions_list(request, workshop_pk):
    workshop = get_object_or_404(Workshop, pk=workshop_pk)
    questions_list = Question.objects.filter(workshop=workshop)
    questions_list = questions_list.prefetch_related('author', 'author__user')
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
        title = "Feedback"
        msg = 'Attendees can submit their feedback after the completion of the workshop'
        context = {'title': title, 'msg': msg}
        return render(request, 'openclass/info.html', context)
    try:
        registration = Registration.objects.get(
                                        workshop=workshop,
                                        profile=profile
                                        )
        if not registration.present:
            title = "Feedback"
            msg = 'Only attendees can submit a feedback'
            context = {'title': title, 'msg': msg}
            return render(request, 'openclass/info.html', context)
    except:
        title = "Feedback"
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
        mc_questions = workshop.mc_questions.all().prefetch_related('choices')
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
        new_choices = []
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
                new_choices.append(choice_pk)
        feedback.choices.add(*new_choices)
        title = 'Feedback submitted'
        msg = 'Thank you, your feedback has been submitted'
        context = {'title': title, 'msg': msg}
        return render(request, 'openclass/info.html', context)

def user_questions(request):
    questions = Question.objects.filter(author=request.user.profile)
    questions = questions.prefetch_related('workshop')
    context = {"questions": questions}
    return render(request, "openclass/user-questions.html", context)
