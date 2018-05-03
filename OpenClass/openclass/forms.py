from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Workshop

class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'birthday', 'phone_number', 'interests', 'photo']

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

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
