from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Employer(Base):
    """SQLAlchemy model for an employer."""
    __tablename__ = 'employers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    contact_email = Column(String(255))
    industry = Column(String(255))
    jobs = relationship("Job", back_populates="employer", lazy="joined")

class Job(Base):
    """SQLAlchemy model for a job posting."""
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(String(255))
    employer_id = Column(Integer, ForeignKey('employers.id'))
    employer = relationship("Employer", back_populates="jobs", lazy="joined")

    applications = relationship("JobApplication", back_populates="job", lazy="joined")

class User(Base):
    """SQLAlchemy model for a user."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    password_hash = Column(String)
    role = Column(String)

    applications = relationship("JobApplication", back_populates="user", lazy="joined")

class JobApplication(Base):
    """SQLAlchemy model for a job application."""
    __tablename__ = 'job_applications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

    user = relationship("User", back_populates="applications", lazy="joined")
    job = relationship("Job", back_populates="applications", lazy="joined")