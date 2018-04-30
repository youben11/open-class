from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
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

    def test_update_first_name(self):
        self.assertEqual(self.profile.user.first_name, '')
        self.profile.update_first_name('ayoub')
        self.assertEqual(self.profile.user.first_name, 'ayoub')
        self.profile.update_first_name('')
        self.assertEqual(self.profile.user.first_name, 'ayoub')

    def test_update_last_name(self):
        self.assertEqual(self.profile.user.last_name, '')
        self.profile.update_last_name('benaissa')
        self.assertEqual(self.profile.user.last_name, 'benaissa')
        self.profile.update_last_name('')
        self.assertEqual(self.profile.user.last_name, 'benaissa')

    def test_ask(self):
        self.profile.ask(self.workshop.id, "What does RE mean ?")
        question = self.profile.asked.all()[0]
        self.assertEqual(question.question, "What does RE mean ?")

class WorkshopTest(TestCase):
    """Workshop model test cases"""

    @classmethod
    def setUp(self):
        Workshop.objects.create(
                        title='PWNign in user_land',
                        description="exploit dev",
                        required_materials="laptop, linux OS",
                        objectives="debuggin, exploit dev",
                        requirements="C programming, Linux basics",
                        seats_number=99,
                        submission_date=datetime.now(),
                        decision_date=datetime.now(),
                        start_date=datetime.now(),
                        duration=datetime.now() - datetime.now(),
                        location='amphi c',
                        status=Workshop.DONE)


    def test_update_title(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_title = "kernel exploitation"
        old_title = w.title
        ret = w.update_title(new_title)
        self.assertEqual(ret, True)
        self.assertEqual(w.title, new_title)

        # MAX_LEN_TITLE condition
        new_title = "A"*(Workshop.MAX_LEN_TITLE+1)
        old_title = w.title
        ret = w.update_title(new_title)
        self.assertEqual(ret, False)
        self.assertEqual(w.title, old_title)

        # blank title
        new_title = ""
        old_title = w.title
        ret = w.update_title(new_title)
        self.assertEqual(ret, False)
        self.assertEqual(w.title, old_title)

    def test_update_description(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_description = "learn how to find bugs and dev exploits"
        old_description = w.description
        ret = w.update_description(new_description)
        self.assertEqual(ret, True)
        self.assertEqual(w.description, new_description)

        # blank description
        new_description = ""
        old_description = w.description
        ret = w.update_description(new_description)
        self.assertEqual(ret, False)
        self.assertEqual(w.description, old_description)

    def test_update_required_materials(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_required_materials = "linux os, gdb-peda, radare2"
        old_required_materials = w.objectives
        ret = w.update_required_materials(new_required_materials)
        self.assertEqual(ret, True)
        self.assertEqual(w.required_materials, new_required_materials)

        # blank objectives
        new_required_materials = ""
        old_required_materials = w.required_materials
        ret = w.update_required_materials(new_required_materials)
        self.assertEqual(ret, False)
        self.assertEqual(w.required_materials, old_required_materials)

    def test_objectives(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_objectives = "secure coding, bug exploitation"
        old_objectives = w.objectives
        ret = w.update_objectives(new_objectives)
        self.assertEqual(ret, True)
        self.assertEqual(w.objectives, new_objectives)

        # blank objectives
        new_objectives = ""
        old_objectives = w.objectives
        ret = w.update_objectives(new_objectives)
        self.assertEqual(ret, False)
        self.assertEqual(w.objectives, old_objectives)

    def test_update_requirements(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_requirements = "python, c, assembly"
        old_requirements = w.requirements
        ret = w.update_requirements(new_requirements)
        self.assertEqual(ret, True)
        self.assertEqual(w.requirements, new_requirements)

        # blank requirements
        new_requirements = ""
        old_requirements = w.requirements
        ret = w.update_requirements(new_requirements)
        self.assertEqual(ret, False)
        self.assertEqual(w.requirements, old_requirements)

    def test_update_seats_number(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_seats_number = 64
        old_seats_number = w.seats_number
        ret = w.update_seats_number(new_seats_number)
        self.assertEqual(ret, True)
        self.assertEqual(w.seats_number, new_seats_number)

        # zero seats_number
        new_seats_number = 0
        old_seats_number = w.seats_number
        ret = w.update_seats_number(new_seats_number)
        self.assertEqual(ret, False)
        self.assertEqual(w.seats_number, old_seats_number)

        # negative number
        new_seats_number = -15
        old_seats_number = w.seats_number
        ret = w.update_seats_number(new_seats_number)
        self.assertEqual(ret, False)
        self.assertEqual(w.seats_number, old_seats_number)

    def test_update_start_date(self):
        w = Workshop.objects.all()[0]
        timezone = w.start_date.tzinfo

        # normal update
        new_start_date = datetime.now(timezone) + timedelta(5)
        old_start_date = w.start_date
        ret = w.update_start_date(new_start_date)
        self.assertEqual(ret, True)
        self.assertEqual(w.start_date, new_start_date)

        # date without timezone
        new_start_date = datetime.now() + timedelta(5)
        old_start_date = w.start_date
        ret = w.update_start_date(new_start_date)
        self.assertEqual(ret, False)
        self.assertEqual(w.start_date, old_start_date)

        # old date
        new_start_date = datetime.now(timezone) - timedelta(16)
        old_start_date = w.start_date
        ret = w.update_start_date(new_start_date)
        self.assertEqual(ret, False)
        self.assertEqual(w.start_date, old_start_date)

    def test_update_location(self):
        w = Workshop.objects.all()[0]

        # normal update
        new_location = "class prepa amphi B"
        old_location = w.location
        ret = w.update_location(new_location)
        self.assertEqual(ret, True)
        self.assertEqual(w.location, new_location)

        # MAX_LEN_location condition
        new_location = "A"*(Workshop.MAX_LEN_LOCATION+1)
        old_location = w.location
        ret = w.update_location(new_location)
        self.assertEqual(ret, False)
        self.assertEqual(w.location, old_location)

        # blank location
        new_location = ""
        old_location = w.location
        ret = w.update_location(new_location)
        self.assertEqual(ret, False)
        self.assertEqual(w.location, old_location)
