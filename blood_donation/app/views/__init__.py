from strawberry.django.views import GraphQLView
from .donor import Donor_Mutation, Donor_Query
from .admin import Admin_Mutation, Admin_Query
import strawberry


class Mutation(Donor_Mutation, Admin_Mutation):
    pass


class Query(Admin_Query, Donor_Query):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)


def graphql_request(request):
    graphql_view = GraphQLView.as_view(schema=schema)
    return graphql_view(request)