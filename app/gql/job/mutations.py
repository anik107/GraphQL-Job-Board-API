from graphene import Mutation, String, Int, Field
from app.gql.types import JobObject
from app.db.database import Session
from app.db.models import Job

class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        with Session() as session:
            job = Job(
                title=title,
                description=description,
                employer_id=employer_id
            )
            session.add(job)
            session.commit()
            session.refresh(job)
            return AddJob(job=job)

class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        with Session() as session:
            job = session.query(Job).filter(Job.id == job_id).first()
            if not job:
                raise Exception("Job not found")

            if title is not None:
                job.title = title
            if description is not None:
                job.description = description
            if employer_id is not None:
                job.employer_id = employer_id

            session.commit()
            session.refresh(job)
            session.close()
            return UpdateJob(job=job)

class DeleteJob(Mutation):
    class Arguments:
        job_id = Int(required=True)

    success = String()

    @staticmethod
    def mutate(root, info, job_id):
        with Session() as session:
            job_id = session.query(Job).filter(Job.id == job_id).first()
            if not job_id:
                raise Exception("Job not found")
            session.delete(job_id)
            session.commit()
            session.close()
            return DeleteJob(success="Job deleted successfully")
