import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "🔥 Test Start Message\n\n"
        "This is a premium emoji test:\n"
        "<tg-emoji emoji-id=\"5298727558711629080\">🔥</tg-emoji>\n\n"
        "If you see animation → Premium ✅\n"
        "If not → Normal user 🙂"
    )
    await message.answer(text, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
