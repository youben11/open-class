from django.db import models

class Workshop(models.Model):
    title = models.TextField()
    description = models.TextField()
    material_required = models.TextField()
    what_u_will_learn = models.TextField()
    nb_places = models.PositiveIntegerField()
    date = models.DateTimeField()
    location = models.TextField()
    cover_img = models.ImageField()
    accepted = models.BooleanField()


class Registration(models.Model):
    date = models.DateField()
    confirmed = models.BooleanField()

class Question(models.Model):
    question = models.TextField()

class Feedback(models.Model):
    feedback = models.TextField()

class Tag(models.Model):
    name = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField() #choice here
    score = models.PositiveIntegerField()
    phone_number = models.TextField()
    date_birth = models.DateField()
    confirmation_value = models.TextField()
    confirmed = models.BooleanField()
    photo = models.ImageField()
    enrollement_date = models.DateField()

class Preference(models.Model):
    confidentiality = models.IntegerField()

class Badge(models.Model):
    name = models.TextField()
    description = models.TextField()
    img = models.ImageField()

    class Meta:
        abstract = True

class Have_badge(models.Model):
    priority = models.PositiveIntegerField()
