import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from db import create_table
from handlers import router
from config import *

bot = Bot(
    token=TG_TOKEN,
    default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
)
dp = Dispatcher()

async def main():
    await create_table()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")