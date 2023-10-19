from pydantic import BaseModel


class User(BaseModel):
    user_pokemon: str
    computer_pokemon: str
    data: str
    winner: str


class Email(BaseModel):
    to_email: str
    subject: str
    message: str


class Pokemon(BaseModel):
    name: str
    height: int
    hp: int
    attack: int
    defence: int
    speed: int
    picture: str
