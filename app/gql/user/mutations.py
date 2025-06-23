from graphene import Mutation, String, Field
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject
from app.utils import generate_token, hash_password, verify_password, get_authenticated_user

class LoginUser(Mutation):
    """Mutation to log in a user."""

    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        """Mutate method to log in a user."""
        with Session() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                raise GraphQLError("Invalid email or password")
            if not verify_password(password, user.password_hash):
                raise GraphQLError("Invalid email or password")
            token = generate_token(user.email)
            return LoginUser(token=token)

class AddUser(Mutation):
    """Mutation to add a new user."""

    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user_info = Field(lambda: UserObject)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        """Mutate method to add a new user."""
        if role == "admin":
            user = get_authenticated_user(info.context)
            if not user or user.role != "admin":
                raise GraphQLError("Only admins can add new users")

        with Session() as session:
            existing_user = session.query(User).filter(User.email == email).first()
            if existing_user:
                raise GraphQLError("User with this email already exists")

            password_hash = hash_password(password)
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            session.close()
            return AddUser(user_info=user)