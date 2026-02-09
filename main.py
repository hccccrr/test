from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import re
import json
import os

bot = Bot("8263898247:AAEjfKb2d8PdGLefAVBk7TdHtm0Q81Cot8o")
dp = Dispatcher()

EMOJI_FILE = "emojis.json"

DEFAULT_EMOJIS = [
    {"id": "6334598469746952256", "fallback": "🌸"},
    {"id": "6082358463541809815", "fallback": "😳"},
    {"id": "6073197143680619201", "fallback": "🤍"},
    {"id": "6073590322166763941", "fallback": "🎈"},
    {"id": "6070852396479683965", "fallback": "❤"}
]

def load_emojis():
    if os.path.exists(EMOJI_FILE):
        try:
            with open(EMOJI_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_EMOJIS
    return DEFAULT_EMOJIS

def save_emojis(emojis):
    try:
        with open(EMOJI_FILE, 'w', encoding='utf-8') as f:
            json.dump(emojis, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def parse_emoji(text):
    pattern = r'<tg-emoji emoji-id="(\d+)">(.+?)</tg-emoji>'
    match = re.search(pattern, text)
    if match:
        return {"id": match.group(1), "fallback": match.group(2)}
    return None

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    emojis = load_emojis()
    
    emoji_text = "Test "
    for emoji in emojis:
        emoji_text += f'<tg-emoji emoji-id="{emoji["id"]}">{emoji["fallback"]}</tg-emoji> '
    
    # Simple buttons (without colors)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="😎 Blue", callback_data="blue"),
            InlineKeyboardButton(text="🔥 Red", callback_data="red"),
            InlineKeyboardButton(text="💚 Green", callback_data="green")
        ],
        [
            InlineKeyboardButton(text="Default Button", callback_data="default")
        ]
    ])
    
    await message.answer(
        emoji_text.strip(),
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.message(Command("buttons"))
async def colored_buttons_cmd(message: types.Message):
    """Colored buttons with custom emoji (Bot API 9.4)"""
    
    # Create keyboard data manually for colored buttons
    keyboard_json = {
        "inline_keyboard": [
            [
                {
                    "text": "😎 Blue",
                    "callback_data": "blue_colored",
                    "style": "blue"  # NEW: Button background color
                },
                {
                    "text": "🔥 Red",
                    "callback_data": "red_colored",
                    "style": "red"
                },
                {
                    "text": "💚 Green",
                    "callback_data": "green_colored",
                    "style": "green"
                }
            ],
            [
                {
                    "text": "Default Button",
                    "callback_data": "default_colored"
                    # No style = default gray
                }
            ]
        ]
    }
    
    await message.answer(
        "Choose a colored button:",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text="😎 Blue", callback_data="blue"),
                    types.InlineKeyboardButton(text="🔥 Red", callback_data="red"),
                    types.InlineKeyboardButton(text="💚 Green", callback_data="green")
                ],
                [
                    types.InlineKeyboardButton(text="Default", callback_data="default")
                ]
            ]
        )
    )
    
    # Note: Colored buttons currently need raw API call
    # Aiogram doesn't fully support 'style' parameter yet

@dp.message(Command("advanced"))
async def advanced_buttons_cmd(message: types.Message):
    """Advanced colored buttons using raw API"""
    
    # Manual API call for colored buttons
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "😎 Blue", "callback_data": "blue", "style": "blue"},
                {"text": "🔥 Red", "callback_data": "red", "style": "red"},
                {"text": "💚 Green", "callback_data": "green", "style": "green"}
            ],
            [
                {"text": "Default Button", "callback_data": "default"}
            ]
        ]
    }
    
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Advanced colored buttons (Bot API 9.4):",
            reply_markup=keyboard
        )
    except Exception as e:
        await message.answer(f"Error: {e}\n\nNote: Colored buttons require Bot API 9.4 and premium bot owner.")

@dp.message(Command("add"))
async def add_emoji_cmd(message: types.Message):
    command_text = message.text.strip()
    emoji_part = command_text.replace("/add", "", 1).strip()
    
    if not emoji_part:
        await message.answer("❌ Use: /add <tg-emoji emoji-id=\"123\">😊</tg-emoji>")
        return
    
    emoji_data = parse_emoji(emoji_part)
    
    if not emoji_data:
        await message.answer("❌ Invalid emoji format. Ignored.")
        return
    
    emojis = load_emojis()
    
    if any(e["id"] == emoji_data["id"] for e in emojis):
        await message.answer("⚠️ Emoji already exists!")
        return
    
    emojis.append(emoji_data)
    
    if save_emojis(emojis):
        await message.answer(
            f'✅ Emoji added: <tg-emoji emoji-id="{emoji_data["id"]}">{emoji_data["fallback"]}</tg-emoji>',
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Error saving emoji.")

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
        await message.answer("✅ Reset to defaults!")
    else:
        await message.answer("❌ Error resetting.")

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    await callback.answer(f"You clicked: {callback.data}")
    await callback.message.answer(f"✅ Selected: {callback.data}")

async def main():
    print("Bot started with colored button support!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
