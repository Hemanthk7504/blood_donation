import strawberry
from django.contrib.auth.hashers import make_password
from ..models.admin_model import Admin


@strawberry.type
class AdminType:
    id: int
    username: str
    email: str
    hospital_name: str
    address: str
    Name: str
    mobile: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_admin(self,
                     username: str, email: str, hospital_name: str, address: str,
                     password: str, name: str, mobile: str
                     ) -> AdminType:
        hashed_password = make_password(password)
        admin = Admin.objects.create(
            username=username, email=email, hospital_name=hospital_name,
            address=address, password=hashed_password, Name=name, mobile=mobile
        )
        return AdminType(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            hospital_name=admin.hospital_name,
            address=admin.address,
            Name=admin.Name,
            mobile=admin.mobile
        )


@strawberry.type
class Query:
    @strawberry.field
    def admin(self, username: str) -> AdminType:
        try:
            admin = Admin.objects.get(username=username)
            return AdminType(
                id=admin.id,
                username=admin.username,
                email=admin.email,
                hospital_name=admin.hospital_name,
                address=admin.address,
                Name=admin.Name,
                mobile=admin.mobile
            )
        except Admin.DoesNotExist:
            return None


schema = strawberry.Schema(query=Query, mutation=Mutation)
