from fastapi_notes_api.app.services.user_service import create_user
from fastapi_notes_api.app.schemas.user import UserCreate

user = create_user(UserCreate(
    username="Kattie",
    email="Stephan_Rau55@hotmail.com",
    password="mU5s8rDvou92ViU")
)

print(user)
