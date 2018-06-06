from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import User
import re


def validate_birthday(birthday):
    diff = timezone.now().date() - birthday
    years = diff.days / 365
    if years < 13:
        raise ValidationError(
                    _("you must be at least 13 years old"),
                    code='invalid'
                    )

class UserFormValidator:
    def clean_username(self):
        username_re = "^[a-zA-Z0-9@.+-_]{1,20}$"
        username = self.cleaned_data.get('username', False)
        if username:
            if not re.match(username_re, username):
                raise ValidationError(
                            _("invalid username"),
                            code='invalid'
                            )
            try:
                user = User.objects.get(username=username)
                raise ValidationError(
                            _("this username is already taken"),
                            code='invalid'
                            )
            except User.DoesNotExist:
                pass
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        if email:
            try:
                user = User.objects.get(email=email)
                raise ValidationError(
                            _("this email is already taken"),
                            code='invalid'
                            )
            except User.DoesNotExist:
                pass
        return email
