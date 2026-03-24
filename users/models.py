from email.policy import default
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField( null=True)
    bio = models.CharField(max_length=140, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)