from django.core.mail import EmailMessage
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from theapp.predefined import ADMIN_TYPE_TWO, ADMIN_TYPE_ONE

from n1sp.celery import app
from theapp.models import EmailVerification
from theapp.models import Approval
from theapp.models import User


@app.task
def post_signup_processing(user, host):

    # Send email confirmation
    send_email_confirmation.delay(user, host)

    # Create approval records for this user
    admin_t2 = User.objects.filter(groups__name=ADMIN_TYPE_TWO).first()
    admin_t1 = User.objects.filter(groups__name=ADMIN_TYPE_ONE).first()
    Approval.objects.create(
        for_user=user,
        by_admin=admin_t2,
        admin_type=Group.objects.get(name=ADMIN_TYPE_TWO)
    )
    Approval.objects.create(
        for_user=user,
        by_admin=admin_t1,
        admin_type=Group.objects.get(name=ADMIN_TYPE_ONE)
    )


@app.task
def send_email_confirmation(user, host):
    # Delete old tokens
    EmailVerification.objects.filter(user=user).delete()

    # Generate a fresh email verification token
    ev = EmailVerification.objects.create(user=user)

    subject = 'Please confirm your email by clicking\
    the given link'
    link = 'http://' + host + \
        reverse('email-confirm', kwargs={'token': ev.token})
    content = "Please confirm your email: %s" % link
    msg = EmailMessage(subject, content,
                       from_email=settings.DEFAULT_FROM_EMAIL,
                       to=[user.email])
    msg.content_subtype = 'HTML'
    msg.send(fail_silently=False)
    print('Sent email confirmation link mail to %s' % user.username)
