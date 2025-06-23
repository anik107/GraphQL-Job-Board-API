from graphene import Mutation, String, Field, Int
from app.gql.types import EmployerObject
from app.db.models import Employer
from app.db.database import Session
from app.db.database import Session
from app.utils import get_authenticated_user

class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer_info = Field(lambda: EmployerObject)

    # temporary
    authenticated_as = Field(String)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        user = get_authenticated_user(info.context)
        with Session() as session:
            employer = Employer(
                name=name,
                contact_email=contact_email,
                industry=industry
            )
            session.add(employer)
            session.commit()
            session.refresh(employer)
            session.close()
            return AddEmployer(employer_info=employer, authenticated_as=user.email)

class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer_info = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):
        with Session() as session:
            employer = session.query(Employer).filter(Employer.id == employer_id).first()
            if not employer:
                raise Exception("Employer not found")

            if name is not None:
                employer.name = name
            if contact_email is not None:
                employer.contact_email = contact_email
            if industry is not None:
                employer.industry = industry

            session.commit()
            session.refresh(employer)
            return UpdateEmployer(employer_info=employer)

class DeleteEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)

    success = String()

    @staticmethod
    def mutate(root, info, employer_id):
        with Session() as session:
            employer = session.query(Employer).filter(Employer.id == employer_id).first()
            if not employer:
                raise Exception("Employer not found")

            session.delete(employer)
            session.commit()
            session.close()
            return DeleteEmployer(success="Employer deleted successfully")