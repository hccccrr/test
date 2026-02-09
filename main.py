from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    # Just use regular emoji
    await message.answer('Test 🔥', parse_mode="HTML")

# Add this handler to discover valid emoji IDs
@dp.message()
async def echo_emoji(message: types.Message):
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                await message.answer(f"Custom emoji ID: {entity.custom_emoji_id}")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
