import uuid
from django.db import models
from django.contrib.auth.models import User


class DonorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=120)
    Name = models.CharField(max_length=20)
    email = models.CharField(max_length=30,unique=True)
    mobile = models.CharField(max_length=12,unique=True)
    blood_type = models.CharField(max_length=5)
    dob = models.CharField(max_length=20)
    gender = models.CharField(max_length=12)
    weight = models.FloatField()
    address = models.CharField(max_length=100)
