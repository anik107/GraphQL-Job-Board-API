from graphene import Int, ObjectType, List, Field
from sqlalchemy.orm import joinedload
from app.db.database import Session
from app.db.models import Employer, Job, JobApplication, User
from app.gql.types import EmployerObject, JobApplicationObject, JobObject, UserObject

class Query(ObjectType):
    """Root query type for the GraphQL schema."""
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_users(root, info):
        """Resolve the list of users."""
        return Session().query(User).all()
    @staticmethod
    def resolve_employer(root, info, id):
        """Resolve a single employer by ID."""
        return Session().query(Employer).options(joinedload(Employer.jobs)).filter(Employer.id == id).first()
    @staticmethod
    def resolve_job(root, info, id):
        """Resolve a single job by ID."""
        return Session().query(Job).options(joinedload(Job.employer)).filter(Job.id == id).first()
    @staticmethod
    def resolve_jobs(root, info):
        """Resolve the list of jobs."""
        return Session().query(Job).options(joinedload(Job.employer)).all()
    @staticmethod
    def resolve_employers(root, info):
        """Resolve the list of employers."""
        return Session().query(Employer).options(joinedload(Employer.jobs)).all()
    @staticmethod
    def resolve_job_applications(root, info):
        """Resolve a single job application by ID."""
        return Session().query(JobApplication).options(
            joinedload(JobApplication.job),
            joinedload(JobApplication.user)).all()