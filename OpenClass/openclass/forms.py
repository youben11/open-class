from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Workshop, Question, Preference, Link
from .validators import UserFormValidator


class UserSettingsForm(ModelForm, UserFormValidator):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileSettingsFrom(ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['phone_number', 'birthday', 'interests', 'photo']
        widgets = {
                'birthday': forms.DateInput(attrs={'type':'date'}),
                }

class UserPrefsForm(ModelForm):

    class Meta:
        model = Preference
        exclude = ['profile']

class ProfileForm(ModelForm):
    photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['gender', 'birthday', 'phone_number', 'interests', 'photo']
        widgets = {
                'birthday': forms.DateInput(attrs={'type':'date'}),
                }


class UserForm(ModelForm, UserFormValidator):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
                'password':forms.PasswordInput()
        }
        help_texts = {
            'username': '20 characters or fewer. Letters, digits and @/./+/-/_ only.',
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
                'topics',
                'duration',
                'cover_img',
                ]
        widgets = {
                'start_date': forms.DateInput(attrs={'type':'date'}),
                'duration': forms.TextInput(attrs={'placeholder':'HH:MM:SS'})
                }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question']


class LinkForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(LinkForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Link
        fields = ['type', 'url']

    def clean_type(self):
        type = self.cleaned_data.get('type', False)
        if type:
            try:
                profile = self.profile
                link = Link.objects.get(profile=profile, type=type)
                raise ValidationError(
                            _("you can't have two link of the same type"),
                            code='invalid'
                            )
            except Link.DoesNotExist:
                pass
        return type
