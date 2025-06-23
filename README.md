<<<<<<< HEAD
# GraphQL-Job-Board-API
=======
# GraphQL Job Board API

A FastAPI-based GraphQL API for managing employers and job postings. This project demonstrates a complete GraphQL implementation with CRUD operations, database integration, and a modern Python web framework.

## 🚀 Features

- **GraphQL API** with queries and mutations
- **CRUD operations** for Employers and Jobs
- **PostgreSQL database** integration with SQLAlchemy ORM
- **RESTful endpoints** alongside GraphQL
- **Interactive GraphQL Playground** for testing
- **Database seeding** with sample data
- **Modular architecture** with clear separation of concerns

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Usage](#api-usage)
- [GraphQL Schema](#graphql-schema)
- [Development](#development)
- [Contributing](#contributing)

## 📁 Project Structure

```
graphql/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── db/
│   │   ├── __init__.py
│   │   ├── data.py            # Sample data for seeding
│   │   ├── database.py        # Database configuration and session
│   │   └── models.py          # SQLAlchemy models
│   ├── gql/
│   │   ├── __init__.py
│   │   ├── mutations.py       # Root mutation class
│   │   ├── queries.py         # Root query class
│   │   ├── types.py           # GraphQL type definitions
│   │   ├── employer/
│   │   │   ├── __init__.py
│   │   │   ├── mutations.py   # Employer-specific mutations
│   │   │   ├── queries.py     # Employer-specific queries
│   │   │   └── types.py       # Employer-specific types
│   │   └── job/
│   │       ├── __init__.py
│   │       ├── mutations.py   # Job-specific mutations
│   │       ├── queries.py     # Job-specific queries
│   │       └── types.py       # Job-specific types
│   └── settings/
│       ├── __init__.py
│       └── config.py          # Database and app configuration
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🔧 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd graphql
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🗄️ Database Setup

1. **Create a PostgreSQL database:**
   ```sql
   CREATE DATABASE graphql;
   ```

2. **Update database configuration:**
   Edit `app/settings/config.py` and update the database URI:
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/graphql'
   ```

3. **Database initialization:**
   The database tables and sample data will be automatically created when you first run the application.

## 🚀 Running the Application

1. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application:**
   - **GraphQL Playground:** http://localhost:8000/graphql
   - **REST Endpoints:**
     - http://localhost:8000/employers
     - http://localhost:8000/jobs

## 🔍 API Usage

### GraphQL Endpoints

The GraphQL endpoint is available at `/graphql` and includes an interactive playground for testing queries and mutations.

### REST Endpoints

- `GET /employers` - Retrieve all employers
- `GET /jobs` - Retrieve all job postings

### Sample GraphQL Queries

**Get all employers with their jobs:**
```graphql
query {
  employers {
    id
    name
    contactEmail
    industry
    jobs {
      id
      title
      description
    }
  }
}
```

**Get a specific job with employer information:**
```graphql
query {
  job(id: 1) {
    id
    title
    description
    employer {
      name
      industry
    }
  }
}
```

### Sample GraphQL Mutations

**Add a new employer:**
```graphql
mutation {
  addEmployer(
    name: "New Tech Company"
    contactEmail: "contact@newtech.com"
    industry: "Technology"
  ) {
    employerInfo {
      id
      name
      contactEmail
      industry
    }
  }
}
```

**Add a new job:**
```graphql
mutation {
  addJob(
    title: "Frontend Developer"
    description: "Build amazing user interfaces"
    employerId: 1
  ) {
    job {
      id
      title
      description
      employer {
        name
      }
    }
  }
}
```

**Update an employer:**
```graphql
mutation {
  updateEmployer(
    employerId: 1
    name: "Updated Company Name"
    industry: "Updated Industry"
  ) {
    employerInfo {
      id
      name
      industry
    }
  }
}
```

**Delete a job:**
```graphql
mutation {
  deleteJob(jobId: 1) {
    success
  }
}
```

## 📊 GraphQL Schema

### Types

**EmployerObject:**
- `id: Int`
- `name: String`
- `contactEmail: String`
- `industry: String`
- `jobs: [JobObject]`

**JobObject:**
- `id: Int`
- `title: String`
- `description: String`
- `employerId: Int`
- `employer: EmployerObject`

### Queries

- `employers: [EmployerObject]` - Get all employers
- `employer(id: Int!): EmployerObject` - Get employer by ID
- `jobs: [JobObject]` - Get all jobs
- `job(id: Int!): JobObject` - Get job by ID

### Mutations

**Employer Mutations:**
- `addEmployer(name: String!, contactEmail: String!, industry: String!): AddEmployer`
- `updateEmployer(employerId: Int!, name: String, contactEmail: String, industry: String): UpdateEmployer`
- `deleteEmployer(employerId: Int!): DeleteEmployer`

**Job Mutations:**
- `addJob(title: String!, description: String!, employerId: Int!): AddJob`
- `updateJob(jobId: Int!, title: String, description: String, employerId: Int): UpdateJob`
- `deleteJob(jobId: Int!): DeleteJob`

## 🧪 Development

### Adding New Features

1. **Models:** Add new SQLAlchemy models in `app/db/models.py`
2. **Types:** Define GraphQL types in `app/gql/types.py` or create new type files
3. **Queries:** Add new queries in `app/gql/queries.py` or respective query modules
4. **Mutations:** Add new mutations in the appropriate mutation modules
5. **Data:** Update sample data in `app/db/data.py` if needed

### Code Organization

- **Database layer:** `app/db/` - Contains models, database configuration, and data
- **GraphQL layer:** `app/gql/` - Contains GraphQL types, queries, and mutations
- **Configuration:** `app/settings/` - Application settings and configuration
- **Main application:** `app/main.py` - FastAPI app setup and routing

### Key Dependencies

- **FastAPI:** Modern Python web framework
- **Graphene:** Python GraphQL framework
- **SQLAlchemy:** Python SQL toolkit and ORM
- **Starlette-GraphQL:** GraphQL integration for FastAPI
- **psycopg2:** PostgreSQL adapter for Python
- **Uvicorn:** Lightning-fast ASGI server

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 Notes

- The application automatically recreates the database schema on startup (drops and creates tables)
- Sample data includes 2 employers and 4 jobs for testing purposes
- All database sessions are properly managed with context managers
- The GraphQL playground is available in development mode for easy testing

## 🐛 Troubleshooting

**Database connection issues:**
- Ensure PostgreSQL is running
- Check database credentials in `app/settings/config.py`
- Verify the database exists

**Import errors:**
- Make sure you're in the virtual environment
- Install all dependencies from `requirements.txt`

**Port conflicts:**
- The application runs on port 8000 by default
- Use `--port` flag to specify a different port: `uvicorn app.main:app --port 8080`

---

Happy coding! 🎉
>>>>>>> 7a7265b (initial commit)
