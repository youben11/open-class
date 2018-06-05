from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_birthday(birthday):
    diff = timezone.now().date() - birthday
    years = diff.days / 365
    if years < 13:
        raise ValidationError("you must be at least 13 years old.")
