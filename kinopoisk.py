import aiohttp
from urllib.parse import quote as url_encode
from config import *

types = {
    "animated-series": "Мультсериал",
    "anime": "Аниме",
    "cartoon": "Мультфильм",
    "movie": "Фильм",
    "tv-series": "Сериал",
}

def format_film(film):
    if not film:
        return None
    text = (f"🎞 <b>{types[film['type']]}: {film['name']} ({film['year']})</b>\n"
            f"Страна: {film['countries'][0]['name']}\n"
            f"Жанр: {" ".join([genre['name'] for genre in film["genres"]])}\n"
            f"Длительность: {film['movieLength']} мин\n\n"
            f"{film['description']}\n{film['poster']['url']}")
    return text

async def get_request(method: str, params: dict):
    params_list = []
    for key in params.keys():
        if type(params[key]) == list:
            for el in params[key]:
                params_list += [f"{key}={el}"]
        else:
            params_list += [f"{key}={params[key]}"]
    params_text = "&".join(params_list)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://api.kinopoisk.dev{method}?{params_text}",
            headers={"X-API-KEY": KP_TOKEN}
        ) as response:
            r = await response.json()

    return r

async def get_film(type="", genre="", year="", country="", length=""):
    params = {
        "status": "completed",
        "notNullFields": ["type", "name", "year", "countries.name", "genres.name", "description", "movieLength",
                          "poster.url"]}
    if type:
        params['type'] = type
    if genre:
        params['genres.name'] = url_encode(genre)
    if country:
        params['countries.name'] = url_encode(country)
    if length:
        params['movieLength'] = length
    if year:
        params['year'] = year
    film = await get_request(
        method="/v1.4/movie/random",
        params=params
    )
    return format_film(film)

async def get_random_film():
    film = await get_request(
        method="/v1.4/movie/random",
        params={
            "status": "completed",
            "notNullFields": ["type", "name", "year", "countries.name", "genres.name", "description", "movieLength", "poster.url"]
        })
    return format_film(film)

menu = {
        "Страна": ["countries.name", "стран"],
        "Жанр": ["genres.name", "жанров"],
    }

async def get_list(name: str):
    menu_list = await get_request(
        method="/v1/movie/possible-values-by-field",
        params={"field": menu[name][0]}
    )
    return [el['name'] for el in menu_list]

async def get_menu_list(name: str):
    text = f"<b>Список {menu[name][1]}:</b>\n"
    text += "\n".join(await get_list(name))
    return text