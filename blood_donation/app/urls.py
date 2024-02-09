from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from strawberry.django.views import AsyncGraphQLView
from .views import admin,donor,donor_test,donor_login

urlpatterns = [
    path('register/', donor.registration_view, name='register'),
    path('graphql/', donor.graphql_request, name='graphql'),
    path('activate/<str:token>/', donor.activate, name='activate'),
    path('login/', donor_login.login_view, name='login'),

]
