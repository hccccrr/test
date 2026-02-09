from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import re
import json
import os

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

# File to store emojis
EMOJI_FILE = "emojis.json"

# Default emojis
DEFAULT_EMOJIS = [
    {"id": "6334598469746952256", "fallback": "🌸"},
    {"id": "6082358463541809815", "fallback": "😳"},
    {"id": "6073197143680619201", "fallback": "🤍"},
    {"id": "6073590322166763941", "fallback": "🎈"},
    {"id": "6070852396479683965", "fallback": "❤"}
]

def load_emojis():
    """Load emojis from file or return defaults"""
    if os.path.exists(EMOJI_FILE):
        try:
            with open(EMOJI_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_EMOJIS
    return DEFAULT_EMOJIS

def save_emojis(emojis):
    """Save emojis to file"""
    try:
        with open(EMOJI_FILE, 'w', encoding='utf-8') as f:
            json.dump(emojis, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def parse_emoji(text):
    """Extract emoji-id from tg-emoji tag"""
    pattern = r'<tg-emoji emoji-id="(\d+)">(.+?)</tg-emoji>'
    match = re.search(pattern, text)
    if match:
        return {"id": match.group(1), "fallback": match.group(2)}
    return None

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    emojis = load_emojis()
    
    # Create message with all emojis
    emoji_text = "I am Bad "
    for emoji in emojis:
        emoji_text += f'<tg-emoji emoji-id="{emoji["id"]}">{emoji["fallback"]}</tg-emoji> '
    
    await message.answer(emoji_text.strip(), parse_mode="HTML")

@dp.message(Command("add"))
async def add_emoji_cmd(message: types.Message):
    # Get text after /add command
    command_text = message.text.strip()
    
    # Remove /add from the beginning
    emoji_part = command_text.replace("/add", "", 1).strip()
    
    if not emoji_part:
        await message.answer("❌ Use: /add <tg-emoji emoji-id=\"123\">😊</tg-emoji>")
        return
    
    # Parse emoji
    emoji_data = parse_emoji(emoji_part)
    
    if not emoji_data:
        await message.answer("❌ Invalid emoji format. Ignored.")
        return
    
    # Load current emojis
    emojis = load_emojis()
    
    # Check if emoji already exists
    if any(e["id"] == emoji_data["id"] for e in emojis):
        await message.answer("⚠️ Emoji already exists!")
        return
    
    # Add new emoji
    emojis.append(emoji_data)
    
    # Save
    if save_emojis(emojis):
        await message.answer(f'✅ Emoji added: <tg-emoji emoji-id="{emoji_data["id"]}">{emoji_data["fallback"]}</tg-emoji>', parse_mode="HTML")
    else:
        await message.answer("❌ Error saving emoji. Try again.")

@dp.message(Command("list"))
async def list_emojis_cmd(message: types.Message):
    emojis = load_emojis()
    
    if not emojis:
        await message.answer("No emojis saved.")
        return
    
    emoji_text = "Saved emojis:\n\n"
    for i, emoji in enumerate(emojis, 1):
        emoji_text += f'{i}. <tg-emoji emoji-id="{emoji["id"]}">{emoji["fallback"]}</tg-emoji>\n'
    
    await message.answer(emoji_text, parse_mode="HTML")

@dp.message(Command("clear"))
async def clear_emojis_cmd(message: types.Message):
    if save_emojis(DEFAULT_EMOJIS):
        await message.answer("✅ Emoji list reset to defaults!")
    else:
        await message.answer("❌ Error resetting emojis.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
