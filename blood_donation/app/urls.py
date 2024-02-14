from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from strawberry.django.views import AsyncGraphQLView
from .views import admin, donor, donor_test, donor_login, home
#
urlpatterns = [
     path("blood_donation/graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),

#
]
