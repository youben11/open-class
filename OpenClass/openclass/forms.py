from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'birthday', 'phone_number', 'interests', 'photo']

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
