from django.db import models
from django.contrib.auth.models import AbstractUser
from .city import City


class User(AbstractUser):
    """
    Custom user model,
    with one additional field: `location`
    """

    location = models.ForeignKey(City)
