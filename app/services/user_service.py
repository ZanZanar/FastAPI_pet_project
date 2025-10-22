from fastapi_notes_api.app.models.database import engine
from fastapi_notes_api.app.models.model import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from passlib.hash import pbkdf2_sha256
import hashlib

Session = sessionmaker(engine)

def hash_email(email: str) -> str:
    
    normalized_email = email.strip().lower() 
    return hashlib.sha256(normalized_email.encode('utf-8')).hexdigest()

def hash_password(password: str) -> str:
        
    hashed = pbkdf2_sha256.hash(password)
    return hashed

def verify_password(password:str, hashed:str)-> bool:
    
    return pbkdf2_sha256.verify(password, hashed)
    
    
    
def get_user_by_username(username:str)-> User | None:
    
    with Session() as session:
        
        statement = select(User).where(User.username==username)
        result = session.execute(statement).scalar_one_or_none()
        return result        
def create_user(user_data) -> User:

    hashed_password = hash_password(user_data.password)
    hashed_email = hash_email(user_data.email)

    user = User(
        username=user_data.username,
        hashed_email=hashed_email,
        hashed_password=hashed_password
    )

    with Session() as session:
        try:
            session.add(user)
            session.commit()
            session.refresh(user)  
        except Exception:
            print("Ошибка при создании пользователя:" )
            session.rollback()
            raise

    return user