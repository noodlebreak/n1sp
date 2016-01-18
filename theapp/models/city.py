from django.db import models


class City(models.Model):
    """
    Location model - store some locales
    """
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
