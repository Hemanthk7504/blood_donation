import threading
from venv import logger
import strawberry
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from ..models.donor_model import DonorProfile
from uuid import UUID
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

import logging
import qrcode

_request_data = threading.local()


def set_request(request):
    setattr(_request_data, 'request', request)


def get_request():
    return getattr(_request_data, 'request', None)


@csrf_exempt
def register_donor(request):
    set_request(request)
    graphql_view = GraphQLView.as_view(schema=donor_schema)
    return graphql_view(request)


@strawberry.type
class UserType:
    id: UUID
    username: str
    email: str
    blood_type: str
    two_fa_enabled: bool


@strawberry.type
class Donor_Mutation:
    @strawberry.mutation
    def create_donor(self, username: str, password: str, confirm_password: str,
                     email: str, first_name: str, last_name: str, mobile: str, blood_type: str,
                     dob: str, gender: str, weight: float, address: str, enable_two_fa: bool
                     ) -> UserType:
        if password != confirm_password:
            raise Exception('Passwords do not match')
        if DonorProfile.objects.filter(email=email).exists():
            raise Exception('Email already taken')

        if DonorProfile.objects.filter(username=username).exists():
            raise Exception('Username already taken')
        if DonorProfile.objects.filter(mobile=mobile).exists():
            raise Exception('Mobile Number already taken')

        try:
            with transaction.atomic():
                hashed_password = make_password(password)
            donor_profile = DonorProfile.objects.create(
                username=username,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                blood_type=blood_type,
                dob=dob,
                gender=gender,
                weight=weight,
                address=address,
                two_fa_enabled=enable_two_fa
            )

            if enable_two_fa:
                qr_code = qrcode.make(donor_profile.get_two_fa_secret_key())
                donor_profile.two_fa_qr_code = qr_code
                donor_profile.save()

            send_activation_email(instance=donor_profile, created=True)

            return UserType(
                id=donor_profile.id,
                username=donor_profile.username,
                email=donor_profile.email,
                blood_type=donor_profile.blood_type,
                two_fa_enabled=donor_profile.two_fa_enabled
            )

        except Exception as e:
            logger.error("Error creating donor profile: {}".format(e))
            raise Exception({"message": str(e)})


@strawberry.type
class Donor_Query:

    @strawberry.field
    def user(self, username: str) -> UserType:
        try:
            donor = DonorProfile.objects.get(username=username)
            return UserType(
                id=donor.id,
                username=donor.username,
                email=donor.email,
                blood_type=donor.blood_type,
                two_fa_enabled=donor.two_fa_enabled
            )
        except DonorProfile.DoesNotExist:
            return UserType(
                id=0,
                username="",
                email=""
            )


donor_schema = strawberry.Schema(query=Donor_Query, mutation=Donor_Mutation)


def graphql_request(request):
    graphql_view = GraphQLView.as_view(schema=donor_schema)
    return graphql_view(request)


def registration_view(request):
    set_request(request)
    return render(request, 'Donor_register.html')


@receiver(post_save, sender=DonorProfile)
def send_activation_email(instance, created, **kwargs):
    if created:
        donor_id = str(instance.id)

        domain = '127.0.0.1:8000'  # Replace with your actual domain
        protocol = 'http'  # Replace with 'https' if you use SSL/TLS
        activation_url = reverse('activate', kwargs={'token': donor_id})
        activation_url = f'{protocol}://{domain}{activation_url}'

        subject = 'Activate Your Blood Donation Account'
        message = f"Dear {instance.first_name},\n\nThank you for registering!\n\nPlease click the link below to activate your account:\n\n{activation_url}\n\nBest regards,\nYour Blood Donation Team"
        from_email = 'hk265740@gmail.com'
        to_email = instance.email

        # Render the HTML content from the template
        html_message = render_to_string('activation_email.html', {'activation_link': activation_url})

        # Create an EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[to_email],
        )

        # Attach the HTML content to the email
        email.attach_alternative(html_message, "text/html")

        # Send the email
        email.send()


from django.http import HttpResponseServerError


def activate(request, token):
    try:
        donor_id = UUID(token)

        donor = DonorProfile.objects.get(id=donor_id)
        donor.is_active = True
        donor.save()

        return redirect('login')  # Redirect to login page

    except DonorProfile.DoesNotExist:
        return render(request, 'activation_error.html')

    except ValueError:
        return render(request, 'activation_error.html')

    except Exception as e:
        print("An error occurred during activation:", e)
        return HttpResponseServerError("An error occurred during activation. Please try again later.")
