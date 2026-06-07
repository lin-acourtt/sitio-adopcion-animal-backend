from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.admin import Admin
from database.session import get_db

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Authentication functions 

# Hash password
def hash_password(password:str) -> str:
    """It returns the password hashed using argon2 algorithm."""
    return pwd_context.hash(password)

# Authenticate user

def authenticate_user(username: str, password: str, db: Session):
    """It returns the user if the username and password are correct, otherwise it returns None."""
    user = db.query(Admin).filter_by(username=username).first()
    print(f"Password: {password}")
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user