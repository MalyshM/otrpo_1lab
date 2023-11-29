from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, \
    text, create_engine, Text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
def connect_db():
    DATABASE_URL = "postgresql://postgres:admin@db/otrpo_proj"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = Column(String(255))
    password = Column(String)
    email = Column(String(255))
    date_of_add = Column(DateTime)


class PokemonBattle(Base):
    __tablename__ = 'pokemon_battle'

    id = Column(Integer, primary_key=True, server_default=text("nextval('pokemon_battle_id_seq'::regclass)"))
    data = Column(String(255))
    user_pokemon = Column(String(255))
    computer_pokemon = Column(String(255))
    winner = Column(String(255))
    date_of_round = Column(DateTime)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), ForeignKey('users.id'))

    user = relationship('User', primaryjoin='PokemonBattle.user_id == User.id')
