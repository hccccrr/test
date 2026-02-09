from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        'Test Emojis:\n'
        '<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji> '
        '<tg-emoji emoji-id="5375296873982604963">🔥</tg-emoji> '
        '<tg-emoji emoji-id="5377399046906378511">❤️</tg-emoji> '
        '<tg-emoji emoji-id="5314250708464273466">😂</tg-emoji> '
        '<tg-emoji emoji-id="5334696654146754134">🎉</tg-emoji>\n'
        '<tg-emoji emoji-id="5334738606963531730">💯</tg-emoji> '
        '<tg-emoji emoji-id="5314212091719597261">😎</tg-emoji> '
        '<tg-emoji emoji-id="5368317179021502463">🥳</tg-emoji> '
        '<tg-emoji emoji-id="5314326105742764664">😍</tg-emoji> '
        '<tg-emoji emoji-id="5314250708464273467">🤣</tg-emoji>\n'
        '<tg-emoji emoji-id="6334598469746952256">🌸</tg-emoji> '
        '<tg-emoji emoji-id="5314335350027352284">⚡</tg-emoji> '
        '<tg-emoji emoji-id="5314254952028009444">🚀</tg-emoji> '
        '<tg-emoji emoji-id="5314339737476156818">💎</tg-emoji> '
        '<tg-emoji emoji-id="5314315488637408598">🎯</tg-emoji>',
        parse_mode="HTML"
    )

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
