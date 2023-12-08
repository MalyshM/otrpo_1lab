from pydantic import BaseModel


class UserBattle(BaseModel):
    user_pokemon: str
    computer_pokemon: str
    data: str
    winner: str
    token: str | None = None


class Email(BaseModel):
    to_email: str
    subject: str
    message: str

# a
class Pokemon(BaseModel):
    name: str
    height: int
    hp: int
    attack: int
    defence: int
    speed: int
    picture: str


class UserRegistration(BaseModel):
    username: str
    password: str
    email: str


class UserLogin(BaseModel):
    username: str
    password: str
    email: str


class TokenData(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
