from uuid import UUID
import strawberry

@strawberry.type
class UserType:
    id: UUID
    username: str
    email: str
    blood_type: str