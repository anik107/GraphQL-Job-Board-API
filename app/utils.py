from datetime import datetime, timedelta
from datetime import timezone
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
import jwt
from app.db.database import Session
from app.db.models import User
from app.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES

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
    if not auth_header:
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