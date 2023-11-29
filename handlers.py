import ast
import asyncio
from datetime import datetime, timedelta
import json
import random
import time
from typing import Annotated

import jwt
import aiohttp as aiohttp
from fastapi import APIRouter, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.expression import and_
from starlette import status
from starlette.exceptions import HTTPException

import redis
from send_mail import send_email
from models import connect_db, PokemonBattle, User
from ftp import save_pokemon_to_FTP
from schemas import Pokemon, UserRegistration, UserBattle, Email, UserLogin, TokenData
from util_tools import fetch, Hasher
from redis import connect_to_redis_true

router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/api/search', name='Search:search', status_code=status.HTTP_200_OK,
            tags=["Search"], description=
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
                              'save_pokemon': "Save pokemon to FTP"})
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list
    # print(names)


@router.get('/api/pagination', name='Pagination:pagination', status_code=status.HTTP_200_OK,
            tags=["Pagination"], description=
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
    redis = await connect_to_redis_true()
    # await redis.flushdb()
    try:
        cached_response = await redis.get(str((offset // 20) + 1))
        res = ast.literal_eval(cached_response)
        if res is not None:
            print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
            await redis.close()
            return res
    except:
        pass
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
    await redis.set(str((offset // 20) + 1), str(response_list), ex=3600)
    # cached_response= await redis.get(str((offset // 20) + 1))
    # print(cached_response)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    await redis.close()
    return response_list


@router.post('/api/save_battle_round', name='Battle:save_battle_round', status_code=status.HTTP_200_OK, tags=["Battle"])
async def save_battle_round(user: UserBattle, db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    print(user.data)
    print(user.user_pokemon)
    print(user.computer_pokemon)
    if user.token is not None:
        user_from_db = await get_current_user_dev(user.token)
        db.add(PokemonBattle(data=user.data, user_pokemon=user.user_pokemon, computer_pokemon=user.computer_pokemon,
                             date_of_round=datetime.now().date(), winner=user.winner, user_id=user_from_db.id))
    else:
        db.add(PokemonBattle(data=user.data, user_pokemon=user.user_pokemon, computer_pokemon=user.computer_pokemon,
                             date_of_round=datetime.now().date(), winner=user.winner))
    db.commit()
    db.close()
    return 'success'


# print(names)

@router.post('/api/save_pokemon_to_ftp', name='FTP:save_pokemon_to_ftp', status_code=status.HTTP_200_OK, tags=["FTP"])
async def save_pokemon_to_ftp(pokemon: Pokemon):
    res = await save_pokemon_to_FTP(pokemon)
    print(res)
    return res


@router.get('/api/get_all_battle_saves', name='Battle:get_all_battle_saves', status_code=status.HTTP_200_OK,
            tags=["Battle"])
async def get_all_battle_saves(db=Depends(connect_db)):
    # Create your plot using Plotly
    result = db.query(PokemonBattle).all()
    db.close()
    return result


# Registration and login standard
# region
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/api/registration_standard', name='Registration:registration_standard', status_code=status.HTTP_200_OK,
             tags=["Registration"])
async def registration_standard(user: UserRegistration, db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    checkuser = db.query(User).filter(and_(User.username == user.username, User.email == user.email)).first()
    if checkuser is not None:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Вам не взломать пентагон")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "password": user.password, "email": user.email},
        expires_delta=access_token_expires
    )
    db.add(User(username=user.username, password=Hasher.get_password_hash(user.password), email=user.email,
                date_of_add=datetime.now().date()))
    db.commit()
    db.close()
    print({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}


def get_user(username, email):
    db = connect_db()
    res = db.query(User).filter(and_(User.username == username, User.email == email)).first()
    db.close()
    return res


@router.post('/api/get_current_user', name='User:get_current_user', status_code=status.HTTP_200_OK, tags=["User"])
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        password: str = payload.get("password")
        email: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, password=password, email=email)
    except:
        raise credentials_exception
    user = get_user(username=token_data.username, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@router.post('/api/get_current_user_dev', name='User:get_current_user_dev', status_code=status.HTTP_200_OK,
             tags=["User"])
async def get_current_user_dev(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("username")
        password: str = payload.get("password")
        email: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, password=password, email=email)
        print(token_data)
    except:
        raise credentials_exception
    user = get_user(username=token_data.username, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@router.get('/api/confirmation_standard', name='Registration:confirmation_standard', status_code=status.HTTP_200_OK,
            tags=["Registration"])
async def confirmation_standard(email: str, db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    print(email)
    password = ""
    for _ in range(4):
        password += str(random.randint(0, 9))
    res = send_email_route(Email(to_email=email, subject='Одноразовый пароль', message=password))
    print(res)
    db.commit()
    db.close()
    if 'successfully' in res['message']:
        return {'user': 'confirmation password has been sent', 'password': password}
    else:
        raise 'error'


@router.get('/api/get_all_users', name='User:get_all_users', status_code=status.HTTP_200_OK, tags=["User"])
async def get_all_users(db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    all_users = db.query(User).all()
    return all_users


@router.get('/api/delete_all_users', name='User:delete_all_users', status_code=status.HTTP_200_OK, tags=["User"])
async def delete_all_users(db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    db.query(User).delete()
    db.commit()
    return {"message": "All users deleted successfully"}


@router.post("/send-email", name='SMTP:send_email_route', status_code=status.HTTP_200_OK, tags=["SMTP"])
def send_email_route(email: Email):
    print(email.to_email)
    print(email.subject)
    print(email.message)
    return send_email(email.to_email, email.subject, email.message)


@router.post('/api/login_standard', name='Registration:login_standard', status_code=status.HTTP_200_OK,
             tags=["Registration"])
async def login_standard(user: UserLogin, db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    checkuser = db.query(User).filter(and_(User.username == user.username, User.email == user.email)).first()
    print(checkuser)
    if checkuser is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Вам не взломать пентагон")
    is_true_login = Hasher.verify_password(user.password, checkuser.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": checkuser.username, "password": checkuser.password, "email": checkuser.email},
        expires_delta=access_token_expires
    )
    db.close()
    if is_true_login:
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return "not logged"


# endregion

# Registration and login oauth2
# region

CLIENT_ID = "asdasdasd"  # Replace with your Yandex OAuth2 client ID
CLIENT_SECRET = "asdasdasd"  # Replace with your Yandex OAuth2 client secret
REDIRECT_URI = "https://oauth.yandex.ru/verification_code"  # Replace with your redirect URI
AUTHORIZE_URL = "https://oauth.yandex.com/authorize"
TOKEN_URL = "https://oauth.yandex.com/token"
USERINFO_URL = "https://login.yandex.ru/info"


@router.post('/api/registration_oauth2', name='Registration Oauth2:registration_oauth2', status_code=status.HTTP_200_OK,
             tags=["Registration Oauth2"])
async def registration_oauth2():
    auth_url = f"{AUTHORIZE_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return {"authorization_url": auth_url}


@router.get("/api/callback", name='Registration Oauth2:callback', status_code=status.HTTP_200_OK,
            tags=["Registration Oauth2"])
async def callback(code: str):
    await asyncio.sleep(0)
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }

    async with AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)
        access_token = response.json().get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        headers = {"Authorization": f"OAuth {access_token}"}
        response = await client.get(USERINFO_URL, headers=headers)
        user_info = response.json()

        # Here, you can process the user_info and perform the registration logic
        # Extract the necessary data like username, email, etc. from the user_info
        print({"user_info": user_info})
        return {"user_info": user_info}

# endregion
