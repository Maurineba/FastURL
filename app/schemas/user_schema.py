from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
   name: str = Field(..., min_length=2, max_length=255)
   email: EmailStr

class UserCreate(UserBase):
   password: str

class UserDelete(BaseModel):
   message: str = "Usuario deletado com sucesso!"

   model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
   id: int


