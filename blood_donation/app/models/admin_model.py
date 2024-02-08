import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template import loader


class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True)
    hospital_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=120)
    Name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
