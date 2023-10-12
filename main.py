import asyncio
import time

import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
from starlette.middleware.cors import CORSMiddleware

from handlers import router, fetch, Email
from send_mail import send_email


def get_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router)
    return application


app = get_application()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pokemon", response_class=HTMLResponse)
async def get_pokemon_a_lot(request: Request, offset: int = None, limit: int = None):
    url = f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            pokemons_data = response.json()
            return templates.TemplateResponse("index.html",
                                              {"request": request, "alter_pokemons": pokemons_data["results"]})


@app.get("/battle")
async def battle(request: Request, userPokemon: str, randomPokemon: str):
    # Perform the battle logic using the user's Pokemon and random Pokemon names
    response_list = []
    start_time = time.time()
    url = 'https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0'
    headers = {'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    timeout = aiohttp.ClientTimeout(total=30)
    conn = aiohttp.TCPConnector(limit_per_host=20)
    name_to_find_list = [userPokemon, randomPokemon]
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
            for pokemon in name_to_find_list:
                if name['name'] in pokemon:
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
    print(response_list)
    # Render the battle template with the relevant data
    return templates.TemplateResponse("battle.html",
                                      {"request": request, "userPokemon": response_list[0],
                                       "randomPokemon": response_list[1]})


@app.post("/send-email")
def send_email_route(email:Email):
    print(email.to_email)
    print(email.subject)
    print(email.message)
    return send_email(email.to_email, email.subject, email.message)


if __name__ == "__main__":
    import uvicorn
    import webbrowser

    uvicorn.run(app, host="localhost", port=8090, log_level="info", access_log=False)
