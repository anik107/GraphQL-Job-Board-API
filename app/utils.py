from datetime import datetime, timedelta
from datetime import timezone
from functools import wraps
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
import jwt
from app.db.database import Session
from app.db.models import User
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRATION_TIME_MINUTES = int(os.getenv("TOKEN_EXPIRATION_TIME_MINUTES"))

def generate_token(email):
    """Generate a JWT token for the user."""
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def hash_password(password):
    """Hash a password using the Argon2 algorithm."""
    ph = PasswordHasher()
    return ph.hash(password)

def verify_password(password, hashed_password):
    """Verify a password against a hashed password."""
    try:
        ph = PasswordHasher()
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False

def get_authenticated_user(context):
    """Placeholder function to get the authenticated user."""
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')
    token = auth_header.split(" ")
    if not auth_header or len(token) != 2 or token[0].lower() != 'bearer':
        raise GraphQLError("Authentication credentials were not provided.")
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], timezone.utc):
            raise GraphQLError("Token has expired.")
        session = Session()
        user = session.query(User).filter(User.email == payload['sub']).first()
        session.close()
        if not user:
            raise GraphQLError("User not found.")
        return user
    except jwt.DecodeError:
        raise GraphQLError("Invalid token.")
    except jwt.InvalidSignatureError:
        raise GraphQLError("Invalid token signature.")
    except jwt.ExpiredSignatureError:
        raise GraphQLError("Token has expired.")
    except jwt.InvalidTokenError:
        raise GraphQLError("Invalid token.")
    except Exception as e:
        raise GraphQLError(f"An error occurred while decoding the token: {str(e)}")

def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        User = get_authenticated_user(args[1].context)
        if not User or User.role != "admin":
            raise GraphQLError("Only admins can perform this action")
        return func(*args, **kwargs)
    return wrapper

def auth_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_authenticated_user(args[1].context)
        return func(*args, **kwargs)
    return wrapper

def auth_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        User = get_authenticated_user(args[1].context)
        uid = kwargs.get('user_id')
        if not User or User.id != uid:
            raise GraphQLError("User not authorized to perform this action")
        return func(*args, **kwargs)
    return wrapper