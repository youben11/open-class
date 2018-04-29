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
    CANCELED = 'C'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REFUSED, 'Refused'),
        (DONE, 'Done'),
        (CANCELED, 'Canceled'),
    )

    registred = models.ManyToManyField('Profile', through='Registration',\
                                        related_name='registred_to')
    mc_questions = models.ManyToManyField('MCQuestion')
    animator = models.ForeignKey('Profile', on_delete=models.SET_NULL,\
                                null=True, related_name='animated')
    topics = models.ManyToManyField('Tag')
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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, db_index=True)

    def update_title(self, new_title):
        if 0 < len(new_title) <= self.MAX_TITLE:
            self.title = new_title
            self.save()
            return True
        else:
            return False

    def update_description(self, new_description):
        if len(new_description) > 0:
            self.description = new_description
            self.save()
            return True
        else:
            return False

    def update_material_required(self, new_material_required):
        if len(new_material_required) > 0:
            self.material_required = new_material_required
            self.save()
            return True
        else:
            return False

    def update_what_u_will_learn(self, new_what_u_will_learn):
        if len(new_what_u_will_learn) > 0:
            self.what_u_will_learn = new_what_u_will_learn
            self.save()
            return True
        else:
            return False

    def update_requirements(self, new_requirements):
        if len(new_requirements) > 0:
            self.requirements = new_what_u_will_learn
            self.save()
            return True
        else:
            return False

    def update_nb_place(self, new_nb_places):
        if new_nb_places > 0:
            self.nb_places = new_nb_places
            self.save()
            return True
        else:
            return False

    def update_date_start(self, new_date_start):
        # all dates must have tzinfo
        timezone = self.date_start.tzinfo
        if new_date_start > datetime.now(timezone):
            self.date_start = new_date_start
            self.save()
            return True
        else:
            return False

    def update_location(self, new_location):
        if 0 < len(new_location) <= self.MAX_LOCATION:
            self.location = new_location
            self.save()
            return True
        else:
            return False

    def update_cover_img(self):
        pass

    def update_topics(self):
        pass

    def get_topics(self):
        pass

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
    PENDING = 'P'
    ACCEPTED = 'A'
    REFUSED = 'R'
    CANCELED = 'C'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REFUSED, 'Refused'),
        (CANCELED, 'Canceled'),
    )

    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    date_registration = models.DateTimeField()
    date_cancel = models.DateTimeField()
    confirmed = models.BooleanField()

class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    question = models.TextField()

class Feedback(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    choices = models.ManyToManyField('Choice')
    submission_date = models.DateTimeField()
    comment = models.TextField()

#Multiple Choice Question
class MCQuestion(models.Model):
    MAX_QST = 20

    question = models.CharField(max_length=MAX_QST)

class Choice(models.Model):
    MAX_CHOICE = 20

    question = models.ForeignKey('MCQuestion', on_delete=models.CASCADE)
    choice = models.CharField(max_length=MAX_CHOICE)

class Tag(models.Model):
    name = models.TextField()

class Profile(models.Model):
    MAX_PHONE_NB = 20
    MAX_CONF_VAL = 64
    MALE = 'M'
    FEMALE = 'F'
    NAG = ' ' #NotAGender
    GENDER_CHOICES = ((MALE, 'Male'),\
                        (FEMALE, 'Female'),\
                        (NAG, ''))
    badges = models.ManyToManyField('Badge', through='Have_badge')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField('Tag')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=NAG)
    score = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=MAX_PHONE_NB)
    date_birth = models.DateField()
    confirmation_value = models.CharField(max_length=MAX_CONF_VAL)
    confirmed = models.BooleanField()
    photo = models.ImageField()
    enrollement_date = models.DateField()

    def workshop_animated(self):
        workshops = self.animated.all()
        return workshops

class Preference(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    confidentiality = models.IntegerField()

class Badge(models.Model):
    MAX_BADGE_NAME = 20
    name = models.CharField(max_length=MAX_BADGE_NAME)
    description = models.TextField()
    img = models.ImageField()


class Have_badge(models.Model):
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

class BadgeAttendance(Badge):
    nb_attendance = models.PositiveIntegerField()

    def is_gained():
        pass
