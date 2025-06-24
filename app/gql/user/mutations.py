from graphene import Mutation, String, Field, Int
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import JobApplication, User
from app.gql.types import JobApplicationObject, UserObject
from app.utils import (
    generate_token,
    hash_password,
    verify_password,
    auth_user_same_as,
    get_authenticated_user,
    auth_user
)
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

class ApplyToJob(Mutation):
    """Mutation to apply to a job."""
    class Arguments:
        job_id = Int(required=True)
        user_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    @auth_user_same_as
    def mutate(root, info, job_id, user_id):
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise GraphQLError("User not found")

            job_application = session.query(JobApplication).filter(
                JobApplication.job_id == job_id,
                JobApplication.user_id == user_id
            ).first()
            if job_application:
                raise GraphQLError("User has already applied to this job")
            job_application = JobApplication(
                job_id=job_id,
                user_id=user_id
            )
            session.add(job_application)
            session.commit()
            session.refresh(job_application)
            session.close()
            return ApplyToJob(job_application=job_application)