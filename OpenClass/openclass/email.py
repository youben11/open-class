from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_verification_mail(user, token):
    SITE_URL = 'http://localhost:8000'

    context = {}
    context['token'] = token
    context['site_url'] = SITE_URL

    subject = "OpenClass Email verification"
    msg = "Here is the link for the validation %s%s" % \
            (SITE_URL, reverse('openclass:verify', kwargs={'token':token}))
    html_msg = render_to_string('openclass/email_verification.html', context)
    to = [user.email,]
    send_mail(subject, msg, settings.EMAIL_HOST_USER, to, html_message=html_msg)
