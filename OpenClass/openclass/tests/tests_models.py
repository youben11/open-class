from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, date
from openclass.models import *

class ModelsTest(TestCase):
    """Tests all models and their relations with each other"""
    @classmethod
    def setUpTestData(cls):
        cls.badge = Badge.objects.create(name='Best Instructor',
                                          description='The best instructor',
                                          img=None)
        cls.profile = Profile(gender='M', score=100,
                                phone_number='+21600000',
                                date_birth=date.today(),
                                verification_value='45abc3',
                                verified=False,
                                photo=None,
                                enrollement_date=date.today(),
                                )
        cls.user = User.objects.create(username='youben11',
                                        email='youben@yopmail.com',
                                        profile=cls.profile)
        cls.profile.user = cls.user
        cls.profile.save()
        cls.workshop = Workshop.objects.create(title='Binary Analysis',
                                                description="Learn how to RE B",
                                                nb_places=100,
                                                date_submission=datetime.now(),
                                                date_decision=datetime.now(),
                                                date_start=datetime.now(),
                                                duration=datetime.now() - datetime.now(),
                                                location='amphi c',
                                                )
        cls.registration = None
        cls.question = None
        cls.feedback = None
        cls.choice = None
        cls.mcquestion = None
        cls.tag = None
        cls.preference = None
        cls.have_badge = None
        cls.badge_attendance = None

    def test_user(self):
        self.assertEqual(self.user.username, 'youben11')
        self.assertEqual(self.user.profile, self.profile)
        self.assertEqual(self.user.profile.verification_value, '45abc3')

class ProfileTest(TestCase):
    """Tests the Profile model and its methods"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
                                username='youben11',
                                email='youben@yopmail.com',
                                )

        cls.profile = Profile.objects.create(
                        gender='M', score=100,
                        phone_number='+21600000',
                        date_birth=date.today(),
                        verification_value='45abc3',
                        verified=False,
                        photo=None,
                        enrollement_date=date.today(),
                        user=cls.user,
                        )
        cls.workshop = Workshop.objects.create(
                        title='Binary Analysis',
                        description="Learn how to RE B",
                        nb_places=100,
                        date_submission=datetime.now(),
                        date_decision=datetime.now(),
                        date_start=datetime.now(),
                        duration=datetime.now() - datetime.now(),
                        location='amphi c',
                        )
        cls.profile.animated.add(cls.workshop)
        cls.registration = Registration.objects.create(
                            workshop=cls.workshop,
                            profile=cls.profile,
                            date_registration=datetime.now(),
                            present=True,
                            status=Registration.ACCEPTED,
                            )

    def test_workshops_animated(self):
        workshop = self.profile.workshops_animated()[0]
        self.assertEqual(workshop.title, 'Binary Analysis')

    def test_workshops_attended(self):
        workshop = self.profile.workshops_attended()[0]
        self.assertEqual(workshop.title, 'Binary Analysis')
