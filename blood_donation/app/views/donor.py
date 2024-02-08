from uuid import UUID

import strawberry
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ..models.donor_model import DonorProfile


@strawberry.type
class UserType:
    id: UUID
    username: str
    email: str
    blood_type: str


@csrf_exempt
@strawberry.type
class Mutation:
    @strawberry.mutation
    @csrf_exempt
    def create_donor(self,
                     username: str, password: str, confirm_password: str,
                     email: str, name: str, mobile: str, blood_type: str,
                     dob: str, gender: str, weight: float, address: str
                     ) -> UserType:
        if password != confirm_password:
            raise Exception('Passwords do not match')

        hashed_password = make_password(password)
        # user = User.objects.create(username=username, password=hashed_password, email=email)

        donor_profile = DonorProfile.objects.create(
            username=username,
            password=hashed_password,
            Name=name,
            email=email,
            mobile=mobile,
            blood_type=blood_type,
            dob=dob,
            gender=gender,
            weight=weight,
            address=address
        )

        return UserType(
            id=donor_profile.id,
            username=donor_profile.username,
            email=donor_profile.email
        )


@strawberry.type
class Query:
    @strawberry.field
    def user(self, username: str) -> UserType:
        try:
            user = DonorProfile.objects.get(username=username)
            return UserType(
                id=user.id,
                username=user.username,
                email=user.email,
                blood_type=user.blood_type
            )

        except User.DoesNotExist:
            # Return a UserType instance with default or empty values
            return UserType(
                id=0,
                username="",
                email=""
            )


donor_schema = strawberry.Schema(query=Query, mutation=Mutation)


def graphql_request(request):
    graphql_view = GraphQLView.as_view(schema=donor_schema)
    return graphql_view(request)


def registration_view(request):
    return render(request, 'Donor_register.html')
