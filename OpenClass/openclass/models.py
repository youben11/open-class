from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class Workshop(models.Model):
    MAX_TITLE = 20
    MAX_LOCATION = 20

    FIFO = 'F'
    MANUAL = 'M'
    POLITIC_CHOICES = (
        (FIFO, 'FIFO'),
        (MANUAL, 'Manual'),
    )

    PENDING = 'P'
    ACCEPTED = 'A'
    REFUSED = 'R'
    DONE = 'D'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REFUSED, 'Refused'),
        (DONE, 'Done'),
    )

    title = models.CharField(max_length=MAX_TITLE)
    description = models.TextField()
    material_required = models.TextField()
    what_u_will_learn = models.TextField()
    requirements = models.TextField()
    nb_places = models.PositiveIntegerField()
    date_submission = models.DateTimeField()
    date_decision = models.DateTimeField()
    date_start = models.DateTimeField()
    duration = models.DurationField()
    registration_politic = models.CharField(max_length=1, choices=POLITIC_CHOICES)
    location = models.CharField(max_length=MAX_LOCATION)
    cover_img = models.ImageField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def accept(self):
        # accept only a PENDING workshop
        if self.status == self.PENDING:
            timezone = self.date_start.tzinfo
            self.date_decision = datetime.now(timezone)
            self.status = self.ACCEPTED
            self.save()
            return True
        else:
            return False

    def is_accepted(self):
        if self.status == self.ACCEPTED:
            return True
        else:
            return False

    def days_left(self):
        timezone = self.date_start.tzinfo
        time_left = self.date_start - datetime.now(timezone)
        return time_left.days   # return only days left


class Registration(models.Model):
    STATUS_CHOICES = []

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    date_registration = models.DateTimeField()
    date_cancel = models.DateTimeField()
    confirmed = models.BooleanField()

class Question(models.Model):
    question = models.TextField()

class Feedback(models.Model):
    submission_date = models.DateTimeField()
    comment = models.TextField()

#Multiple Choice Question
class MCQuestion(models.Model):
    MAX_QST = 20

    question = models.CharField(max_length=MAX_QST)

class Choice(models.Model):
    MAX_CHOICE = 20

    choice = models.CharField(max_length=MAX_CHOICE)

class Tag(models.Model):
    name = models.TextField()

class Profile(models.Model):
    MAX_PHONE_NB = 20
    MAX_CONF_VAL = 64
    MALE = 'M'
    FEMALE = 'F'
    NAG = ' ' #NotAGender
    GENDER_CHOICES = [(MALE, 'Male'),\
                        (FEMALE, 'Female'),\
                        (NAG, '')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=NAG)
    score = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=MAX_PHONE_NB)
    date_birth = models.DateField()
    confirmation_value = models.CharField(max_length=MAX_CONF_VAL)
    confirmed = models.BooleanField()
    photo = models.ImageField()
    enrollement_date = models.DateField()

class Preference(models.Model):
    confidentiality = models.IntegerField()

class Badge(models.Model):
    MAX_BADGE_NAME = 20
    name = models.CharField(max_length=MAX_BADGE_NAME)
    description = models.TextField()
    img = models.ImageField()

    class Meta:
        abstract = True

class Have_badge(models.Model):
    priority = models.PositiveIntegerField()
