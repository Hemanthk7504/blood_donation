# from strawberry.django.views import GraphQLView
# from .donor import Donor_Query
# from .donor import Donor_Mutation
# from .admin import Admin_Mutation, Admin_Query
# from .donor_login import LoginMutation
# import strawberry
#
#
# @strawberry.federation
# class Query(Admin_Query, Donor_Query):
#     pass
#
#
# @strawberry.federation
# class Mutation(Donor_Mutation, Admin_Mutation, LoginMutation):
#     pass
#
#
# schema = strawberry.Schema(query=Query, mutation=Mutation)
#
#
# def graphql_request(request):
#     graphql_view = GraphQLView.as_view(schema=schema)
#     return graphql_view(request)
