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
                                birthday=date.today(),
                                verification_token='45abc3',
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
                                                seats_number=100,
                                                submission_date=datetime.now(),
                                                decision_date=datetime.now(),
                                                start_date=datetime.now(),
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
        self.assertEqual(self.user.profile.verification_token, '45abc3')

class ProfileTest(TestCase):
    """Tests the Profile model and its methods"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
                                username='youben11',
                                )

        cls.profile = Profile.objects.create(
                        gender='M', score=100,
                        phone_number='',
                        birthday=date.today(),
                        verification_token='45abc3',
                        verified=False,
                        photo=None,
                        enrollement_date=date.today(),
                        user=cls.user,
                        )
        cls.profile.update_email('youben@yopmail.com')
        cls.profile.update_phone_number('+213 557 388 000 ')
        cls.workshop = Workshop.objects.create(
                        title='Binary Analysis',
                        description="Learn how to RE B",
                        seats_number=100,
                        submission_date=datetime.now(),
                        decision_date=datetime.now(),
                        start_date=datetime.now(),
                        duration=datetime.now() - datetime.now(),
                        location='amphi c',
                        status=Workshop.DONE,
                        )
        cls.profile.animated.add(cls.workshop)
        cls.registration = Registration.objects.create(
                            workshop=cls.workshop,
                            profile=cls.profile,
                            date_registration=datetime.now(),
                            present=True,
                            status=Registration.ACCEPTED,
                            )
        cls.tag1 = Tag.objects.create(name="AI/ML")
        cls.tag2 = Tag.objects.create(name="Security")
        cls.profile.interests.add(cls.tag1, cls.tag2)


    def test_workshops_animated(self):
        workshop = self.profile.workshops_animated()[0]
        self.assertEqual(workshop.title, 'Binary Analysis')

    def test_workshops_attended(self):
        workshop = self.profile.workshops_attended()[0]
        self.assertEqual(workshop.title, 'Binary Analysis')

    def test_get_interest(self):
        interest = self.profile.get_interests()
        self.assertEqual(interest.get(id=self.tag1.id).name, self.tag1.name)
        self.assertEqual(interest.get(id=self.tag2.id).name, self.tag2.name)

    def test_update_email(self):
        self.assertEqual(self.profile.user.email, 'youben@yopmail.com')

    def test_update_phone_number(self):
        self.assertEqual(self.profile.phone_number, "+213557388000")
        self.profile.update_phone_number('055 7 ')
        self.assertEqual(self.profile.phone_number, "0557")
        self.profile.update_phone_number('055 a 7')
        self.assertEqual(self.profile.phone_number, "0557")
