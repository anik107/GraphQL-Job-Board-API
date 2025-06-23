from graphene import (
    ObjectType,
    String,
    Int,
    List,
    Field,
)

class EmployerObject(ObjectType):
    """GraphQL type representing an employer."""

    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        """Resolve the list of jobs for the employer."""
        return root.jobs

class JobObject(ObjectType):
    """GraphQL type representing a job posting."""

    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        """Resolve the list of applications for the job."""
        return root.applications
    @staticmethod
    def resolve_employer(root, info):
        """Resolve the employer for the job."""
        return root.employer

class UserObject(ObjectType):
    """GraphQL type representing a user."""

    id = Int()
    username = String()
    email = String()
    role = String()

    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        """Resolve the list of applications for the job."""
        return root.applications

class JobApplicationObject(ObjectType):
    """GraphQL type representing a job application."""

    id = Int()
    user_id = Int()
    job_id = Int()

    job = Field(lambda: JobObject)
    user = Field(lambda: UserObject)

    @staticmethod
    def resolve_job(root, info):
        """Resolve the job for the application."""
        return root.job
    @staticmethod
    def resolve_user(root, info):
        """Resolve the user for the application."""
        return root.user
