from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    owner = models.OneToOneField(User, related_name='profile')


class Client(models.Model):
    owner = models.ForeignKey(User, related_name='client')
    registration_id = models.TextField()


class Notification(models.Model):
    owner = models.ForeignKey(User, related_name='owned')
    creator = models.ForeignKey(User, related_name='created')
    body = models.TextField()
