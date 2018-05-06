from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "openclass"

urlpatterns = [
    path('', views.index, name="index"),
    path('workshops/', views.workshops_list, name='workshops_list'),
    path('workshops/<int:pk>/', views.workshops_detail, name='workshops_detail'),
    path('members/', views.members_list, name='members_list'),
    path('members/<int:pk>/', views.members_detail, name='members_detail'),
    path('badges/', views.badges_list, name='badges_list'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
<<<<<<< HEAD
    path('submit_workshop/', views.submit_workshop, name='submit_workshop'),
=======
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.login, name='logout'),
>>>>>>> b2dd0c56323dbd5a9c3549508aff32f201fc684c
]
