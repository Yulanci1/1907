import aiohttp
from bs4 import BeautifulSoup

async def check_slots():
    url = "https://visa.vfsglobal.com/rus/en/fra/login"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    if "Нет доступных дат" in soup.text or "No appointment slots" in soup.text:
        return False

    # Это зависит от текущей структуры сайта
    return True
