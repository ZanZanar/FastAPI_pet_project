from pydantic import BaseModel, Field, EmailStr, field_validator
import re

USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_-]+$")

class UserBase(BaseModel):
    username: str = Field(...,min_length=3,max_length=30,description="Имя пользователя от 3 до 30 символов")
    email: EmailStr = Field(..., description="Почтовый адрес пользователя")

    @field_validator("username",mode="before")
    def strip_username(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Имя пользователя не должно быть пустым")
        if not USERNAME_REGEX.match(v):
            raise ValueError("Имя пользователя может содержать только латинские буквы, цифры, символы '_' и '-'")
        return v
    
    @field_validator("email",mode="before")
    def strip_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise ValueError("Почтовый адрес пользователя не должен быть пустым")
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8,max_length=120, description="Пароль должен содержать минимум 8 символов")


class UserRead(UserBase):
    id: int

    class model_config:
        from_attributes = True