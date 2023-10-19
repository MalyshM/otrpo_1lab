async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.json()
