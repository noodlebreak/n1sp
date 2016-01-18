from django.db import models
from django.utils.crypto import hashlib
from django.utils import timezone

from .user import User


class EmailVerification(models.Model):
    """
    Simple replacement for an otherwise
    more mature allauth's emailaddress model.
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    # def __init__(self, *args, **kwargs):
    #     self.token = self.create_token()
    #     super(EmailVerification, self).__init__(args, kwargs)

    def create_token(self):
        val = (str(timezone.now()) + self.user.email).encode('utf-8')
        return hashlib.sha256(val).hexdigest()

    def confirm(self):
        self.email_verified = True
        self.save()

    def __str__(self):
        return self.user.email
