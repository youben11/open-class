import re
import random
from django.db import models, transaction, DatabaseError
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from .upload import *

from datetime import datetime


class Workshop(models.Model):
    MAX_LEN_TITLE = 20
    MAX_LEN_LOCATION = 20
    INFINITE_SEATS_NB = 0

    POL_FIFO = 'F'
    POL_MANUAL = 'M'
    POLITIC_CHOICES = (
        (POL_FIFO, 'FIFO'),
        (POL_MANUAL, 'Manual'),
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

    registered = models.ManyToManyField('Profile', through='Registration',
                                        related_name='registered_to')
    mc_questions = models.ManyToManyField('MCQuestion')
    animator = models.ForeignKey('Profile', on_delete=models.SET_NULL,
                                null=True, related_name='animated')
    topics = models.ManyToManyField('Tag')
    title = models.CharField(max_length=MAX_LEN_TITLE, blank=False)
    description = models.TextField(blank=False)
    required_materials = models.TextField()
    objectives = models.TextField()
    requirements = models.TextField()
    seats_number = models.PositiveIntegerField()
    submission_date = models.DateTimeField()
    decision_date = models.DateTimeField(null=True)
    start_date = models.DateTimeField()
    duration = models.DurationField()
    registration_politic = models.CharField(
                                max_length=1,
                                choices=POLITIC_CHOICES,
                                default=POL_FIFO)
    location = models.CharField(max_length=MAX_LEN_LOCATION)
    cover_img = models.ImageField(upload_to=upload_to_workshop_cover)
    status = models.CharField(
                    max_length=1,
                    choices=STATUS_CHOICES,
                    default=PENDING,
                    db_index=True)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.title)

    def register(self, profile):
        registration = Registration(workshop=self, profile=profile)
        if self.registration_politic == Workshop.POL_FIFO:
            if self.seats_number == Workshop.INFINITE_SEATS_NB :
                registration.status == Registration.ACCEPTED
                registration.save()
                return True
            else:
                try:
                    with transaction.atomic():
                        registrations = Registration.objects.filter(
                                            workshop=self,
                                            status=Workshop.ACCEPTED,
                                            )
                        if len(registrations) + 1 <= self.seats_number:
                            registration.status = Registration.ACCEPTED
                        registration.save()
                        return True
                except DatabaseError:
                    return False

    def is_registration_open(self):
        if timezone.now() > self.last_registration_date():
            return False
        else:
            return True

    def last_registration_date(self):
        date = self.start_date
        # put restriction here if needed
        return date

    def cancel_registration(self, profile):
        try:
            registration = Registration.objects.get(
                                    profile=profile,
                                    workshop=self,
                                    )
        except Registration.DoesNotExist:
            return False
        if registration.status == Registration.CANCELED:
            return False
        else:
            registration.date_cancel = timezone.now()
            registration.status = Registration.CANCELED
            registration.save()
            return True


    def last_cancel_date(self):
        date = self.start_date
        # put restriction here if needed
        return date

    def update_title(self, new_title):
        if 0 < len(new_title) <= self.MAX_LEN_TITLE:
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

    def update_required_materials(self, new_required_materials):
        if len(new_required_materials) > 0:
            self.required_materials = new_required_materials
            self.save()
            return True
        else:
            return False

    def update_objectives(self, new_objectives):
        if len(new_objectives) > 0:
            self.objectives = new_objectives
            self.save()
            return True
        else:
            return False

    def update_requirements(self, new_requirements):
        if len(new_requirements) > 0:
            self.requirements = new_requirements
            self.save()
            return True
        else:
            return False

    def update_seats_number(self, new_seats_number):
        if new_seats_number > 0:
            self.seats_number = new_seats_number
            self.save()
            return True
        else:
            return False

    def update_start_date(self, new_start_date):
        # all dates must have tzinfo
        timezone_info = self.start_date.tzinfo
        if new_start_date.tzinfo == None:
            return False
        if new_start_date > datetime.now(timezone_info):
            self.start_date = new_start_date
            self.save()
            return True
        else:
            return False

    def update_location(self, new_location):
        if 0 < len(new_location) <= self.MAX_LEN_LOCATION:
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
        if self.status == Workshop.PENDING and self.start_date > timezone.now():
            self.decision_date = timezone.now()
            self.status = Workshop.ACCEPTED
            self.save()
            return True
        else:
            return False

    def refuse(self):
        # refuse only a PENDING workshop
        if self.status == Workshop.PENDING:
            self.decision_date = timezone.now()
            self.status = Workshop.REFUSED
            self.save()
            return True
        else:
            return False

    def is_accepted(self):
        if self.status == Workshop.ACCEPTED:
            return True
        else:
            return False

    def days_left(self):
        addend = 0
        time_left = self.start_date - timezone.now()
        if self.start_date.time() < timezone.now().time() :
            addend = 1
        return time_left.days + addend  # return only days left

    def check_registration(self, profile):
        flags = {}
        try:
            registration = Registration.objects.get(
                                    profile=profile,
                                    workshop=self,
                                    )
        except:
            return flags
        flags['is_pending'] = registration.status == Registration.PENDING
        flags['is_accepted'] = registration.status == Registration.ACCEPTED
        flags['is_refused'] = registration.status == Registration.REFUSED
        flags['is_canceled'] = registration.status == Registration.CANCELED

        return flags

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
    status = models.CharField(
                max_length=1,
                choices=STATUS_CHOICES,
                default=PENDING,
                null=False)
    date_registration = models.DateTimeField(auto_now_add=True)
    date_cancel = models.DateTimeField(null=True)
    present = models.BooleanField(null=False, default=False)

    class Meta:
        unique_together = (('workshop', 'profile'),)

    def __str__(self):
        return "[%02d] %s -> %s <%s>" % (self.pk, self.profile, self.workshop,
                                        self.status)

    def confirm_presence(self):
        #make sure the workshop has started
        self.present = True

class Question(models.Model):
    author = models.ForeignKey(
                    'Profile',
                    on_delete=models.SET_NULL,
                    related_name='asked',
                    null=True)
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    question = models.TextField(blank=False)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.question)

class Feedback(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    workshop = models.ForeignKey('Workshop', on_delete=models.CASCADE)
    choices = models.ManyToManyField('Choice')
    submission_date = models.DateTimeField()
    comment = models.TextField(blank=False)

    class Meta:
        unique_together = (('workshop', 'author'),)

    def __str__(self):
        return "[%02d] %s -> %s" % (self.pk, self.author, self.workshop.title)

#Multiple Choice Question
class MCQuestion(models.Model):
    MAX_LEN_QST = 20

    question = models.CharField(max_length=MAX_LEN_QST, blank=False)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.question)

class Choice(models.Model):
    MAX_LEN_CHOICE = 20

    question = models.ForeignKey('MCQuestion', on_delete=models.CASCADE)
    choice = models.CharField(max_length=MAX_LEN_CHOICE, blank=False)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.choice)

class Tag(models.Model):
    MAX_LEN_NAME = 20
    name = models.CharField(max_length=MAX_LEN_NAME, blank=False)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.name)

class Profile(models.Model):
    RE_PHONE_NB = r"^(\+[\d ]{3})?[\d ]+$"
    MAX_LEN_PHONE_NB = 20
    MALE = 'M'
    FEMALE = 'F'
    NAG = 'X' #NotAGender
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NAG, 'Not mentioned')
    )
    badges = models.ManyToManyField('Badge', through='Have_badge')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField('Tag')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=NAG)
    score = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(
                            max_length=MAX_LEN_PHONE_NB,
                            validators=[RegexValidator(regex=RE_PHONE_NB),])
    birthday = models.DateField(null=True)
    photo = models.ImageField(upload_to=upload_to_profile_photo)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.user)

    def generate_verification_token(self):
        try:
            verification_token = VerificationToken.objects.get(profile=self)
        except VerificationToken.DoesNotExist:
            verification_token = VerificationToken(profile=self)

        token = verification_token.generate_new_token()
        #render and send email
        return token

    def is_registered(self, workshop):
        try:
            registration = Registration.objects.get(
                                    profile=self,
                                    workshop=workshop,
                                    )
            return True
        except Registration.DoesNotExist:
            return False

    def can_cancel_registration(self, workshop):
        if timezone.now() > workshop.last_cancel_date():
            return False

        try:
            registration = Registration.objects.get(
                                    profile=self,
                                    workshop=workshop,
                                    )
        except Registration.DoesNotExist:
            return False

        if registration.status == Registration.ACCEPTED or \
            registration.status == Registration.PENDING:
            return True
        else:
            return False

    def update_email(self, email):
        """Update the user's email only if it is valid.
        Verify the new email by sending the verification_token."""

        email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(email_re, email):
            self.user.email = email
            self.user.save()
            #do the verification: send email...
            return True
        else:
            return False

    def update_phone_number(self, phone_number):
        """Update the user's phone number only if it is valid."""

        phone_nb_re = r"^(\+[0-9]{3})?[0-9]+$"
        phone_number = phone_number.replace(" ","")
        if re.match(phone_nb_re, phone_number):
            self.phone_number = phone_number
            self.save()
            return True
        else:
            return False

    def update_first_name(self, fname):
        """Update the user's first name."""

        if len(fname):
            self.user.first_name = fname
            self.user.save()
            return True
        else:
            return False

    def update_last_name(self, lname):
        """Update the user's last name."""

        if len(lname):
            self.user.last_name = lname
            self.user.save()
            return True
        else:
            return False

    def workshops_animated(self):
        """Get the workshops that the user animated.
        The workshops must be DONE."""

        workshops = self.animated.filter(status=Workshop.DONE)
        return workshops

    def workshops_attended(self):
        """Get the workshops that the user attended, the registration
        must be ACCEPTED and PRESENT (the user was present)."""

        accepted = Q(registration__status=Registration.ACCEPTED)
        present = Q(registration__present=True)
        workshops = self.registered_to.filter(accepted, present)
        return workshops

    def ask(self, workshop_pk, question):
        #check user permission
        #registered?
        try:
            workshop = Workshop.objects.get(pk=workshop_pk)
            registration = Registration.objects.get(
                            workshop=workshop,
                            profile=self)
        except:
            return False

        #present? => accepted ?
        if not registration.present:
            return False

        #is the workshop currently animated?
        start_date = workshop.start_date
        end_date = start_date + workshop.duration
        if start_date < timezone.now() < end_date:
            self.asked.create(workshop=workshop, question=question)
            return True
        else:
            return False


    def get_interests(self):#don't use interests():conflict with field interests
        """Get the user's interests in form of Tags."""

        interests = self.interests.all()
        return interests

    def get_age(self):
        "calculate the age of a user from birthday"
        current_date = timezone.now().date()
        age = current_date.year - self.birthday.year

        if (current_date.month, current_date.day) \
                < (self.birthday.month, self.birthday.day):
            age -= 1

        return age

    def get_registrations(self):
        registrations = Registration.objects.all().filter(profile=self)
        return registrations

class VerificationToken(models.Model):
    TOKEN_LEN = 32

    value = models.CharField(max_length=TOKEN_LEN)
    profile = models.OneToOneField(
                            Profile,
                            related_name='verification_token',
                            on_delete=models.CASCADE,
                            unique=True
                            )

    def generate_new_token(self):
        TOKEN_LEN = VerificationToken.TOKEN_LEN
        CHOICES = "ABCDEF0123456789abcdefg"
        while True:
            token = [random.choice(CHOICES) for i in range(TOKEN_LEN)]
            self.value = "".join(token)
            try: #make sure the token is unique
                v = VerificationToken.objects.get(value=self.value)
            except VerificationToken.DoesNotExist:
                break

        self.save()
        return self.value

    def verify(self, token):
        if token == self.value :
            self.profile.user.is_active = True
            self.profile.user.save()
            self.delete()
            return self.profile.user
        else:
            return None


class Preference(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    confidentiality = models.IntegerField()

class Badge(models.Model):
    MAX_LEN_BADGE_NAME = 20
    name = models.CharField(max_length=MAX_LEN_BADGE_NAME, blank=False)
    description = models.TextField(blank=False)
    img = models.ImageField(upload_to="badges",blank=True,null=True)

    def __str__(self):
        return "[%02d] %s" % (self.pk, self.name)

class Have_badge(models.Model):
    badge = models.ForeignKey('Badge', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

class BadgeAttendance(Badge):
    nb_attendance = models.PositiveIntegerField()

    def is_gained():
        pass
