import asyncio
import datetime
import time
import aiohttp as aiohttp
from fastapi import APIRouter, Query
from sqlalchemy.dialects.postgresql import JSONB
from starlette import status

from models import connect_db, PokemonBattle
from ftp import save_pokemon_to_FTP
from schemas import User, Pokemon
from util_tools import fetch

router = APIRouter()


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
        response1 = await fetch(session=session, url=url)
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
                              'picture': response['sprites']['front_default'],
                              'save_pokemon':"Save pokemon to FTP"})
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
async def pagination(offset: int = None, limit: int = None):
    # Create your plot using Plotly
    response_list = []
    start_time = time.time()
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}'

    headers = {'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    timeout = aiohttp.ClientTimeout(total=30)
    conn = aiohttp.TCPConnector(limit_per_host=20)
    async with aiohttp.ClientSession(trust_env=True, headers=headers, timeout=timeout, connector=conn) as session:
        response1 = await fetch(session=session, url=url)
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
async def save_battle_round(user: User):
    # Create your plot using Plotly
    db = connect_db()
    print(user.data)
    print(user.user_pokemon)
    print(user.computer_pokemon)
    db.add(PokemonBattle(data=user.data, user_pokemon=user.user_pokemon, computer_pokemon=user.computer_pokemon,
                         date_of_round=datetime.datetime.now().date(), winner=user.winner))
    db.commit()
    db.close()
    return 'success'
# print(names)

@router.post('/api/save_pokemon_to_ftp', name='Plot:plot', status_code=status.HTTP_200_OK, tags=["Plot"])
async def save_pokemon_to_ftp(pokemon: Pokemon):
    res= await save_pokemon_to_FTP(pokemon)
    print(res)
    return res