import asyncio
import datetime
import time
import psycopg2
import aiohttp as aiohttp
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import JSONB
from starlette import status

router = APIRouter()

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, \
    text, create_engine, Text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def connect_db():
    DATABASE_URL = "postgresql://postgres:admin@localhost/OTRPO_proj"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


Base = declarative_base()
metadata = Base.metadata


class PokemonBattle(Base):
    __tablename__ = 'pokemon_battle'

    id = Column(Integer, primary_key=True, server_default=text("nextval('category_all_in_one_id_seq'::regclass)"))
    data = Column(String(255))
    date_of_round = Column(DateTime)
    user_pokemon = Column(String(255))
    computer_pokemon = Column(String(255))


class User(BaseModel):
    user_pokemon: str
    computer_pokemon: str
    data: str


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.json()


@router.get('/api/search', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
            """)
async def search(name_to_find: str = None):
    # Create your plot using Plotly
    response_list = []
    start_time = time.time()
    url = 'https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0'
    headers = {'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    timeout = aiohttp.ClientTimeout(total=30)
    conn = aiohttp.TCPConnector(limit_per_host=20)
    async with aiohttp.ClientSession(trust_env=True, headers=headers, timeout=timeout, connector=conn) as session:
        async with session.get(url, ssl=False) as response:
            response1 = await response.json()
        print("--- %s seconds ---" % (time.time() - start_time), end=" get first response\n")
        # print(response1)
        names = response1['results']
        tasks = []
        for name in names:
            # print(name['name'])
            # print(name['name'])
            if name_to_find in name['name']:
                url = name['url']
                task = asyncio.create_task(fetch(session, url))
                tasks.append(task)
            # print(url)
        jsons = await  asyncio.gather(*tasks)
        print("--- %s seconds ---" % (time.time() - start_time), end=" get true response\n")
    for response in jsons:
        response_list.append({'name': response['name'], 'height': response['height'],
                              'hp': response['stats'][0]['base_stat'],
                              'attack': response['stats'][1]['base_stat'],
                              'defence': response['stats'][2]['base_stat'],
                              'speed': response['stats'][5]['base_stat'],
                              'picture': response['sprites']['front_default']})
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list
    # print(names)


@router.get('/api/pagination', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
            """)
async def search(offset: int = None, limit: int = None):
    # Create your plot using Plotly
    response_list = []
    start_time = time.time()
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}'

    headers = {'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    timeout = aiohttp.ClientTimeout(total=30)
    conn = aiohttp.TCPConnector(limit_per_host=20)
    async with aiohttp.ClientSession(trust_env=True, headers=headers, timeout=timeout, connector=conn) as session:
        async with session.get(url, ssl=False) as response:
            response1 = await response.json()
        print("--- %s seconds ---" % (time.time() - start_time), end=" get first response\n")
        # print(response1)
        names = response1['results']
        tasks = []
        for name in names:
            # print(name['name'])
            # print(name['name'])
            url = name['url']
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)
            # print(url)
        jsons = await  asyncio.gather(*tasks)
        print("--- %s seconds ---" % (time.time() - start_time), end=" get true response\n")
    for response in jsons:
        response_list.append({'name': response['name'], 'height': response['height'],
                              'hp': response['stats'][0]['base_stat'],
                              'attack': response['stats'][1]['base_stat'],
                              'defence': response['stats'][2]['base_stat'],
                              'speed': response['stats'][5]['base_stat'],
                              'picture': response['sprites']['front_default'],
                              'choose': 'Выбрать'})

    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list


@router.post('/api/save_battle_round', name='Plot:plot', status_code=status.HTTP_200_OK, tags=["Plot"])
def save_battle_round(user: User):
    # Create your plot using Plotly
    db = connect_db()
    print(user.data)
    print(user.user_pokemon)
    print(user.computer_pokemon)
    db.add(PokemonBattle(data=user.data, user_pokemon=user.user_pokemon, computer_pokemon=user.computer_pokemon, date_of_round=datetime.datetime.now()))
    db.commit()
    db.close()
    return 'success'
# print(names)
