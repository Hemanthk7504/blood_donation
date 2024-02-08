from uuid import UUID
from decouple import config
import strawberry
from django.core.checks import messages
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from ..models.donor_model import DonorProfile
import jws
from uuid import uuid4
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


@strawberry.type
class UserType:
    id: UUID
    username: str
    email: str
    blood_type: str


@strawberry.type
class Donor_Mutation:
    @strawberry.mutation
    def create_donor(self, username: str, password: str, confirm_password: str,
                     email: str, first_name: str, last_name: str, mobile: str, blood_type: str,
                     dob: str, gender: str, weight: float, address: str
                     ) -> UserType:
        if password != confirm_password:
            raise Exception('Passwords do not match')

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
                address=address
            )

            send_activation_email(created=True, instance=donor_profile)

            return UserType(
                id=donor_profile.id,
                username=donor_profile.username,
                email=donor_profile.email,
                blood_type=donor_profile.blood_type
            )

        except Exception as e:
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
                blood_type=donor.blood_type
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
    return render(request, 'Donor_register.html')


@receiver(post_save, sender=DonorProfile)
def send_activation_email(instance, created, **kwargs):
    if created:
        request = kwargs.get("request")
        if not request:
            # Log the error or handle it appropriately
            print("Error: Request object is None")
            return

        token = default_token_generator.make_token(instance)
        domain = '127.0.0.1:8000'  # Replace with your actual domain
        protocol = 'http'  # Replace with 'https' if you use SSL/TLS
        activation_url = reverse('activate', kwargs={'token': token})
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
        if request:
            request.session['activation_token'] = token


def activate(request, token):
    try:
        # Verify the token
        user = default_token_generator.check_token(token)
        if user is None:
            # Token is invalid, redirect to an error page or display a message
            messages.error(request, 'Invalid activation link.')
            return render(request, 'error_page.html')

        # Token is valid, activate the user
        user.is_active = True
        user.save()

        # Log the user in
        # Delete the token from the session
        del request.session['activation_token']

        messages.success(request, 'Your account has been successfully activated. Please login.')
        return render(request, 'activation_success.html')

    except Exception as e:
        return render(request, 'activation_error.html')
