from django.contrib.auth.models import AbstractUser
from django.db import models


class StaffUser(AbstractUser):
    position = models.CharField(verbose_name='Position', max_length=255)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
