from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Workshop
from .models import Registration

class UserSettings(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AttendanceList(ModelForm):
    class meta:
        model = Registration
        presence = forms.BooleanField()
        fields  = ['presence'] 

class UserProfileForm(ModelForm):
    interests = forms.MultipleChoiceField(required=False)
    photo = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['gender', 'birthday', 'phone_number', 'interests', 'photo']
        widgets = {
                'birthday': forms.DateInput(attrs={'type':'date'}),
                }

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
                'password':forms.PasswordInput()
        }

class WorkshopForm(ModelForm):

    class Meta:
        model = Workshop
        fields = [
                'title',
                'description',
                'requirements',
                'objectives',
                'seats_number',
                'required_materials',
                'start_date',
                'duration',
                'cover_img',
                ]
