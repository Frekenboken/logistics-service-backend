from pydantic import BaseModel


class UserResponse(BaseModel):
    email: str
    firstname: str
    lastname: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    expires_in: int
