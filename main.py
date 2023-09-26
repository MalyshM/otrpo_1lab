from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
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
            return templates.TemplateResponse("index.html", {"request": request, "alter_pokemons": pokemons_data["results"]})


if __name__ == "__main__":
    import uvicorn
    import webbrowser

    uvicorn.run(app, host="localhost", port=8000, log_level="info", access_log=False)
