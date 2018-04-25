from django.db import models

class Workshop(models.Model):
    title = #string
    description = #string
    material_required = #string
    what_u_will_learn = #string
    nb_places = #positiveinteger
    date = #date
    location = #string
    cover_img = #image
    accepted = #boolean


class Registration(models.Model):
    date = #date
    confirmed = #boolean

class Question(models.Model):
    question = #string

class Feedback(models.Model):
    feedback = #string

class Tag(models.Model):
    name = #string

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = #enum
    score = #positiveinteger
    phone_number = #string
    date_birth = #date
    confirmation_value = #string
    confirmed = #boolean
    photo = #image
    enrollement_date = #date

class Preference(models.Model):
    confidentiality = #integer

class Badge(models.Model):
    name = #string
    description = #string
    img = #image

    class Meta:
        abstract = True

class Have_badge(models.Model):
    priority = #positiveinteger
