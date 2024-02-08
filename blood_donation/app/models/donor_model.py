from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class DonorProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=120)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    mobile = models.CharField(max_length=12, unique=True)
    blood_type = models.CharField(max_length=5)
    dob = models.DateField()
    gender = models.CharField(max_length=12)
    weight = models.FloatField()
    address = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        managed = True
        default_permissions = ('add', 'change', 'delete')
        default_related_name = 'donorprofile'

    # Added the following lines
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='donorprofile_set',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='donorprofile_set',
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
