import jwt
import strawberry
from django.contrib.auth import authenticate
import jws
from django.core.exceptions import ValidationError
from strawberry.django.views import GraphQLView

from .ty import UserType


@strawberry.type
class AuthPayload:
    token: str
    user: UserType


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def login(self, username: str, password: str) -> AuthPayload:
        try:
            # Authenticate user against DonorProfile model
            user = authenticate(donor_profile__username=username, password=password)
            if user is None:
                raise ValidationError('Invalid username or password')

            # Generate JWT token
            token = jwt.encode({'username': username}, 'secret', algorithm='HS256')

            # Return AuthPayload with token and user info
            return AuthPayload(token=token, user=UserType(id=user.id, username=user.donor_profile.username))

        except ValidationError as e:
            raise Exception(str(e))


@strawberry.type
class Query:
    @strawberry.mutation
    def donor_request(self) -> UserType:
        pass


login_schema = strawberry.Schema(mutation=AuthMutation, query=Query)


def graphql_request(request):
    graphql_view = GraphQLView.as_view(schema=login_schema)
    return graphql_view(request)
