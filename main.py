from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        'Test 🔥 <tg-emoji emoji-id="5298727558711629080">🔥</tg-emoji>',
        parse_mode="HTML"
    )

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
