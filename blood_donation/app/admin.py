from django.contrib import admin
from .models.donor_model import DonorProfile
from django.contrib.auth.admin import UserAdmin


admin.site.register(DonorProfile, UserAdmin)