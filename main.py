from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import json
import os

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

# File to store emoji data
EMOJI_FILE = "emojis_data.json"

# Load or initialize emoji data
def load_emoji_data():
    if os.path.exists(EMOJI_FILE):
        with open(EMOJI_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "premium_enabled": False,
        "custom_emojis": [
            {"id": "6082358463541809815", "fallback": "😬"},
            {"id": "6073197143680619201", "fallback": "🤍"},
            {"id": "6073590322166763941", "fallback": "❤️"},
            {"id": "6070852396479683965", "fallback": "❤️"}
        ],
        "regular_emojis": ['👍', '🔥', '❤️', '😂', '🎉', '💯', '😎', '🥳', '😍', '🤣', '🌸', '⚡', '🚀', '💎', '🎯']
    }

def save_emoji_data(data):
    with open(EMOJI_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

emoji_data = load_emoji_data()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    emoji_data = load_emoji_data()
    
    if emoji_data["premium_enabled"] and emoji_data["custom_emojis"]:
        # Premium emojis show karo
        emoji_text = ""
        for emoji_info in emoji_data["custom_emojis"]:
            emoji_text += f'<tg-emoji emoji-id="{emoji_info["id"]}">{emoji_info["fallback"]}</tg-emoji> '
        
        await message.answer(
            f'Welcome! Here are your premium emojis:\n{emoji_text}',
            parse_mode="HTML"
        )
    else:
        # Regular emojis show karo
        emoji_text = " ".join(emoji_data["regular_emojis"])
        await message.answer(
            f'Welcome! Here are your emojis:\n{emoji_text}',
            parse_mode="HTML"
        )

@dp.message(Command("premium_on"))
async def premium_on(message: types.Message):
    emoji_data = load_emoji_data()
    emoji_data["premium_enabled"] = True
    save_emoji_data(emoji_data)
    
    await message.answer(
        "✅ Premium emojis enabled!\n"
        "Now send me premium emojis and I'll add them automatically."
    )

@dp.message(Command("premium_off"))
async def premium_off(message: types.Message):
    emoji_data = load_emoji_data()
    emoji_data["premium_enabled"] = False
    save_emoji_data(emoji_data)
    
    await message.answer(
        "❌ Premium emojis disabled!\n"
        "Now /start will show regular emojis."
    )

@dp.message(Command("clear_emojis"))
async def clear_emojis(message: types.Message):
    emoji_data = load_emoji_data()
    emoji_data["custom_emojis"] = []
    save_emoji_data(emoji_data)
    
    await message.answer("🗑️ All premium emojis deleted!")

@dp.message(Command("show_ids"))
async def show_ids(message: types.Message):
    emoji_data = load_emoji_data()
    
    if emoji_data["custom_emojis"]:
        ids_text = "Saved Premium Emoji IDs:\n\n"
        for idx, emoji_info in enumerate(emoji_data["custom_emojis"], 1):
            ids_text += f"{idx}. {emoji_info['fallback']} - ID: {emoji_info['id']}\n"
        
        await message.answer(ids_text)
    else:
        await message.answer("No premium emojis saved!")

@dp.message(Command("status"))
async def status(message: types.Message):
    emoji_data = load_emoji_data()
    
    status_text = (
        f"📊 Current Status:\n\n"
        f"Premium Mode: {'✅ ON' if emoji_data['premium_enabled'] else '❌ OFF'}\n"
        f"Saved Premium Emojis: {len(emoji_data['custom_emojis'])}\n"
        f"Regular Emojis: {len(emoji_data['regular_emojis'])}"
    )
    
    await message.answer(status_text)

# Yeh handler custom emoji IDs detect karega
@dp.message(F.entities)
async def get_emoji_ids(message: types.Message):
    emoji_data = load_emoji_data()
    
    if not emoji_data["premium_enabled"]:
        return
    
    custom_emojis_found = []
    
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                # Extract the emoji character
                emoji_char = message.text[entity.offset:entity.offset + entity.length]
                
                emoji_info = {
                    "id": entity.custom_emoji_id,
                    "fallback": emoji_char
                }
                
                # Check if already exists
                if not any(e["id"] == emoji_info["id"] for e in emoji_data["custom_emojis"]):
                    emoji_data["custom_emojis"].append(emoji_info)
                    custom_emojis_found.append(f"{emoji_char} - ID: {entity.custom_emoji_id}")
    
    if custom_emojis_found:
        save_emoji_data(emoji_data)
        await message.answer(
            f"✅ {len(custom_emojis_found)} emoji(s) added!\n\n" +
            "\n".join(custom_emojis_found) +
            "\n\nCheck /start to see the updated message!"
        )

async def main():
    print("Bot is running! 🚀")
    await dp.start_polling(bot)

asyncio.run(main())
