from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import keyboards as kb
import kinopoisk as kp
import db

router = Router()

@router.message(CommandStart())
@router.message(F.text == "🏠 На главную")
async def main_menu(message: Message):
    film = await db.get_settings(message.from_user.id)
    type, genre, year, country, length = film[0]
    await message.answer(
        text=f"<b>Твои предпочтения</b>\n"
             f"Тип: {type}\n"
             f"Жанр: {genre}\n"
             f"Год: {year}\n"
             f"Страна: {country}\n"
             f"Длительность: {length} мин.",
        reply_markup=kb.main
    )

@router.message(F.text == "↩️ Назад")
async def back(message: Message, state: FSMContext):
    await state.set_state(Settings.point)
    await settings(message, state)

@router.message(F.text == "🔍 Поиск")
async def film(message: Message):
    await message.answer(text="Секунду...")

    film = await db.get_settings(message.from_user.id)
    type, genre, year, country, length = film[0]
    film = await kp.get_film(type, genre, year, country, length)

    if film:
        await message.answer_photo(
            photo=film.rsplit("\n", 1)[1],
            caption=film.rsplit("\n", 1)[0],
            reply_markup=kb.film
        )
    else:
        await message.answer(
            text="Фильм не найден",
            reply_markup=kb.main
        )

@router.message(F.text == "🎲 Рандом")
async def random_film(message: Message):
    await message.answer(text="Секунду...")
    film = await kp.get_random_film()
    await message.answer_photo(
        photo=film.rsplit("\n", 1)[1],
        caption=film.rsplit("\n", 1)[0],
        reply_markup=kb.random
    )


class Settings(StatesGroup):
    point = State()
    movieType = State()
    year = State()
    country = State()
    genre = State()
    movieLength = State()

@router.message(F.text == "⚙️ Предпочтения")
async def settings(message: Message, state: FSMContext):
    await state.set_state(Settings.point)
    film = await db.get_settings(message.from_user.id)
    type, genre, year, country, length = film[0]
    await message.answer(
        text=f"<b>⚙️ Предпочтения</b>\n"
             f"Тип: {type}\n"
             f"Жанр: {genre}\n"
             f"Год: {year}\n"
             f"Страна: {country}\n"
             f"Длительность: {length} мин.\n\n"
             f"Выберите раздел с помощью клавиатуры",
        reply_markup=kb.main_settings)

@router.message(F.text == "💾 Сохранить")
async def save(message: Message, state: FSMContext):
    await state.set_state(None)
    await main_menu(message)

@router.message(Settings.point)
async def settings_pt(message: Message, state: FSMContext):
    text = message.text
    if text == "Тип":
        await state.set_state(Settings.movieType)
        await message.answer(text="Укажите тип контента, введя его название\n"
                                  "Например: movie\n"
                                  "Для отчистки отправьте '-'\n\n"
                                  "Посмотреть доступные типы можно, нажав на кнопку ниже",
                             reply_markup=kb.settings_list)
    elif text == "Страна":
        await state.set_state(Settings.country)
        await message.answer(text="Укажите страну производства, введя его название\n"
                                  "Посмотреть доступные страны можно, нажав на кнопку ниже\n"
                                  "Например: США\n"
                                  "Для отчистки отправьте '-'",
                             reply_markup=kb.settings_list)
    elif text == "Жанр":
        await state.set_state(Settings.genre)
        await message.answer(text="Укажите жанр, введя его название\n"
                                  "Посмотреть доступные жанры можно, нажав на кнопку ниже\n"
                                  "Например: комедия\n"
                                  "Для отчистки отправьте '-'",
                             reply_markup=kb.settings_list)
    elif text == "Год":
        await state.set_state(Settings.year)
        await message.answer(text="Укажите год публикации контента\n"
                                  "Например: 2025\n"
                                  "Для отчистки отправьте '-'",
                             reply_markup=kb.settings)
    elif text == "Длительность":
        await state.set_state(Settings.movieLength)
        await message.answer(text="Укажите диапазон длительности контента в минутах\n"
                                  "Например: 90-120\n"
                                  "Для отчистки отправьте '-'",
                             reply_markup=kb.settings)

@router.message(Settings.movieType, F.text == "📋 Вывести список")
async def movieType_list(message: Message):
    await message.answer(
        text=("<b>Список типов:</b>\n"
              "animated-series — Мультсериал\n"
              "anime — Анимация\n"
              "cartoon — Мультфильм\n"
              "movie — Фильм\n"
              "tv-series — Сериал"),
        reply_markup=kb.settings_list
)
@router.message(Settings.movieType)
async def movieType(message: Message, state: FSMContext):
    text = message.text
    if text == "-":
        await db.clear_settings(message.from_user.id, 'type')
        await state.set_state(Settings.point)
        await settings(message, state)
    elif text in [
        "animated-series",
        "anime",
        "cartoon",
        "movie",
        "tv-series"]:
        await db.set_settings(message.from_user.id, type=text)
        await state.set_state(Settings.point)
        await settings(message, state)
    else:
        await message.answer(
            text="Неверно указан тип контента",
            reply_markup=kb.settings_list)

@router.message(Settings.genre, F.text == "📋 Вывести список")
async def genre_list(message: Message):
    text = await kp.get_menu_list("Жанр")
    await message.answer(
        text=text,
        reply_markup=kb.settings_list
)
@router.message(Settings.genre)
async def genre(message: Message, state: FSMContext):
    text = message.text
    if text == "-":
        await db.clear_settings(message.from_user.id, 'genre')
        await state.set_state(Settings.point)
        await settings(message, state)
    elif text in await kp.get_list("Жанр"):
        await db.set_settings(message.from_user.id, genre=text)
        await state.set_state(Settings.point)
        await settings(message, state)
    else:
        await message.answer(
            text="Неверно указан жанр",
            reply_markup=kb.settings_list)

@router.message(Settings.year)
async def year(message: Message, state: FSMContext):
    text = message.text
    if text == "-":
        await db.clear_settings(message.from_user.id, 'year')
        await state.set_state(Settings.point)
        await settings(message, state)
    elif text.isdigit():
        await db.set_settings(message.from_user.id, year=text)
        await state.set_state(Settings.point)
        await settings(message, state)
    else:
        await message.answer(text="Неверно указан год")

@router.message(Settings.country, F.text == "📋 Вывести список")
async def country_list(message: Message):
    text = await kp.get_menu_list("Страна")
    await message.answer(
        text=text,
        reply_markup=kb.settings_list
)
@router.message(Settings.country)
async def country(message: Message, state: FSMContext):
    text = message.text
    if text == "-":
        await db.clear_settings(message.from_user.id, 'country')
        await state.set_state(Settings.point)
        await settings(message, state)
    elif text in await kp.get_list("Страна"):
        await db.set_settings(message.from_user.id, country=text)
        await state.set_state(Settings.point)
        await settings(message, state)
    else:
        await message.answer(
            text="Неверно указана страна",
            reply_markup=kb.settings_list)

@router.message(Settings.movieLength)
async def movieLength(message: Message, state: FSMContext):
    try:
        text = message.text
        if text == "-":
            await db.clear_settings(message.from_user.id, 'length')
            await state.set_state(Settings.point)
            await settings(message, state)
        else:
            map(int, text.split("-"))
            await db.set_settings(message.from_user.id, length=text)
            await state.set_state(Settings.point)
            await settings(message, state)
    except:
        await message.answer("Диапазон указан неверно")