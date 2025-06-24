import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job, User, JobApplication
from app.db.data import employers_data, jobs_data, users_data, applications_data

# Load environment variables from .env file
load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

def prepare_database():
    """Prepare the database by creating tables and inserting initial data."""
    from app.utils import hash_password
    Base.metadata.drop_all(engine)  # Drop existing tables
    Base.metadata.create_all(engine)
    # Create a session
    session = Session()

    for employer in employers_data:
        session.add(Employer(**employer))

    for job in jobs_data:
        session.add(Job(**job))

    for user in users_data:
        user_data = user.copy()
        password = user_data.pop('password')
        user_data['password_hash'] = hash_password(password)
        session.add(User(**user_data))

    for application in applications_data:
        session.add(JobApplication(**application))

    session.commit()
    session.close()