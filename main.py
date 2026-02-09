from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import json
import os

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

EMOJI_FILE = "emojis.json"

def load_emojis():
    if os.path.exists(EMOJI_FILE):
        with open(EMOJI_FILE, 'r') as f:
            return json.load(f)
    return {"premium_on": False, "emojis": []}

def save_emojis(data):
    with open(EMOJI_FILE, 'w') as f:
        json.dump(data, f)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    data = load_emojis()
    
    if data["premium_on"] and data["emojis"]:
        text = "Welcome! "
        for em in data["emojis"]:
            text += f'<tg-emoji emoji-id="{em["id"]}">{em["emoji"]}</tg-emoji> '
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer("Welcome! 👍 🔥 ❤️ 😂 🎉")

@dp.message(Command("premium_on"))
async def premium_on(message: types.Message):
    data = load_emojis()
    data["premium_on"] = True
    save_emojis(data)
    await message.answer("✅ Premium ON! Now send me emojis.")

@dp.message(Command("premium_off"))
async def premium_off(message: types.Message):
    data = load_emojis()
    data["premium_on"] = False
    save_emojis(data)
    await message.answer("❌ Premium OFF!")

@dp.message(F.entities)
async def add_emoji(message: types.Message):
    data = load_emojis()
    
    if not data["premium_on"]:
        return
    
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                emoji_char = message.text[entity.offset:entity.offset + entity.length]
                
                if not any(e["id"] == entity.custom_emoji_id for e in data["emojis"]):
                    data["emojis"].append({"id": entity.custom_emoji_id, "emoji": emoji_char})
                    save_emojis(data)
                    await message.answer(f"✅ Added! Check /start")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
