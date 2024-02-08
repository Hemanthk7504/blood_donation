from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from strawberry.django.views import AsyncGraphQLView
from .views import admin,donor

urlpatterns = [
    path('register/', donor.registration_view, name='register'),
    path('graphql/', donor.graphql_request, name='graphql'),  # Add this line for GraphQL endpoint

]
