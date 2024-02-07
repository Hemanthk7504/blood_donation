import strawberry
from strawberry.django.views import GraphQLView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ..models.donor_model import DonorProfile


@strawberry.type
class UserType:
    id: int
    username: str
    email: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_donor(self,
                     username: str, password: str, confirm_password: str,
                     email: str, name: str, mobile: str, blood_type: str,
                     dob: str, gender: str, weight: float, address: str
                     ) -> UserType:
        if password != confirm_password:
            raise Exception('Passwords do not match')

        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password, email=email)

        donor_profile = DonorProfile.objects.create(
            user=user,
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

        # Return the created user
        return UserType(
            id=user.id,
            username=user.username,
            email=user.email
        )


@strawberry.type
class Query:
    @strawberry.field
    def user(self, username: str) -> UserType:
        try:
            user = User.objects.get(username=username)
            return UserType(
                id=user.id,
                username=user.username,
                email=user.email
            )
        except User.DoesNotExist:
            return {"message": "Donor doesn't Exists"}


donor_schema = strawberry.Schema(query=Query, mutation=Mutation)


def graphql_request(request):
    graphql_view = GraphQLView.as_view(schema=donor_schema)
    return graphql_view(request)


def registration_view(request):
    return render(request, 'Donor_register.html')
