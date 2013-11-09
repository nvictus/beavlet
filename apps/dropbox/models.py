from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    dropbox_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)