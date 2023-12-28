from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
