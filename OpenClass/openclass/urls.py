from django.urls import path, include
from . import views
from django.contrib.auth.views import login, logout


app_name = "openclass"

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('accounts/login', login, name="login"),
    path('accounts/logout', logout, name="logout"),
    path('badges/', views.badges_list, name='badges_list'),
    path('faq/', views.faq, name='faq'),
    path('members/', views.members_list, name='members_list'),
    path('members/<str:username>/', views.members_detail, name='members_detail'),
    path('moderation/', views.moderation, name='moderation'),
    path('moderation/attendance/', views.moderation_attendance, name='moderation_attendance'),
    path('moderation/attendance/<int:workshop_pk>/', views.moderation_workshop_attendance, name='moderation_workshop_attendance'),
    path('moderation/attendance/<int:workshop_pk>/<int:user_pk>/', views.moderation_workshop_user_attendance, name='moderation_workshop_user_attendance'),
    path('moderation/accepted_workshops', views.moderation_accepted_workshops, name='moderation_accepted_workshops'),
    path('moderation/done_workshops', views.moderation_done_workshops, name='moderation_done_workshops'),
    path('moderation/submitted_workshops', views.moderation_submitted_workshops, name='moderation_submitted_workshops'),
    path('moderation/submitted_workshops/decision', views.moderation_submitted_workshops_decision, name='moderation_submitted_workshops_decision'),
    path('moderation/workshops/', views.moderation_workshops, name='moderation_workshops'),
    path('profile/', views.profile, name='profile'),
    path('profile/questions', views.user_questions, name='user_questions'),
    path('profile/preferences', views.prefs, name='prefs'),
    path('profile/registrations', views.user_registrations, name='user_registrations'),
    path('profile/settings', views.user_settings, name='user_settings'),
    path('registration/cancel/', views.cancel_registration, name='cancel_registration'),
    path('signup/', views.signup, name='signup'),
    path('submit_workshop/', views.submit_workshop, name='submit_workshop'),
    path('verify/<token>/', views.verify, name='verify'),
    path('workshops/', views.workshops_list, name='workshops_list'),
    path('workshops/<int:workshop_pk>/', views.workshops_detail, name='workshops_detail'),
    path('workshops/<int:workshop_pk>/ask_question', views.ask_question, name='ask_question'),
    path('workshops/<int:workshop_pk>/feedback', views.feedback, name='feedback'),
    path('workshops/<int:workshop_pk>/questions', views.workshop_questions_list, name='workshop_questions_list'),
    path('workshops/register/',views.register_to_workshop, name='register_to_workshop'),
    path('workshops/tag/', views.workshops_filter_tag, name='workshops_filter_tag'),
    path('workshops/upcoming/', views.upcoming_workshops_list, name='upcoming_workshops_list'),
    #path('workshops/date/<str:filter>/', views.workshops_filter_date, name='workshops_filter_date')


]
