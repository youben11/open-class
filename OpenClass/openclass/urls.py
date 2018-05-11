from django.urls import path, include
from . import views


app_name = "openclass"

urlpatterns = [
    path('', views.index, name="index"),
    path('workshops/', views.workshops_list, name='workshops_list'),
    path('workshops/<int:pk>/', views.workshops_detail, name='workshops_detail'),
    path('members/', views.members_list, name='members_list'),
    path('members/<int:pk>/', views.members_detail, name='members_detail'),
    path('badges/', views.badges_list, name='badges_list'),
    path('profile/', views.profile, name='profile'),
    path('profile/preferences', views.prefs, name='prefs'),
    path('profile/settings', views.user_settings, name='user_settings'),
    path('signup/', views.signup, name='signup'),
    path('submit_workshop/', views.submit_workshop, name='submit_workshop'),
    path('moderation/', views.moderation, name='moderation'),
    path('accounts/', include('django.contrib.auth.urls')),
]
