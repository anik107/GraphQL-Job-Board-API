from graphene import ObjectType
from app.gql.job.mutations import AddJob, UpdateJob, DeleteJob
from app.gql.employer.mutations import AddEmployer, DeleteEmployer, UpdateEmployer
from app.gql.user.mutations import LoginUser, AddUser, ApplyToJob

class Mutation(ObjectType):
    """GraphQL mutation type for adding jobs."""
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUser.Field()
    add_user = AddUser.Field()
    apply_to_job = ApplyToJob.Field()