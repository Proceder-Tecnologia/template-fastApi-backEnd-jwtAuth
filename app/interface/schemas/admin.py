from pydantic import BaseModel, EmailStr

class AdminCreate(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str