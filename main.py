from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import re
import json
import os
import aiohttp
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

async def send_with_emoji_icons(chat_id: int, text: str):
    """Send message with custom emoji icons on buttons"""
    
    url = f"https://api.telegram.org/bot{bot.token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "Blue",
                        "callback_data": "blue",
                        "icon_custom_emoji_id": "6334598469746952256"  # Flower emoji
                    },
                    {
                        "text": "Red",
                        "callback_data": "red",
                        "icon_custom_emoji_id": "6070852396479683965"  # Heart emoji
                    },
                    {
                        "text": "Green",
                        "callback_data": "green",
                        "icon_custom_emoji_id": "6073590322166763941"  # Balloon emoji
                    }
                ],
                [
                    {
                        "text": "Default Button",
                        "callback_data": "default"
                    }
                ]
            ]
        }
    }
    
    logger.info("Sending buttons with custom emoji icons...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                result = await response.json()
                
                if result.get("ok"):
                    logger.info("✅ Success! Buttons sent with custom emoji icons")
                else:
                    logger.error(f"❌ Failed: {result.get('description')}")
                
                return result
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"ok": False, "description": str(e)}

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    emojis = load_emojis()
    
    emoji_text = "Test "
    for emoji in emojis:
        emoji_text += f'<tg-emoji emoji-id="{emoji["id"]}">{emoji["fallback"]}</tg-emoji> '
    
    # Try sending with custom emoji icons
    result = await send_with_emoji_icons(message.chat.id, emoji_text.strip())
    
    if not result.get("ok"):
        # Fallback to regular buttons with emoji in text
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="😎 Blue", callback_data="blue"),
                types.InlineKeyboardButton(text="🔥 Red", callback_data="red"),
                types.InlineKeyboardButton(text="💚 Green", callback_data="green")
            ],
            [
                types.InlineKeyboardButton(text="Default Button", callback_data="default")
            ]
        ])
        
        await message.answer(emoji_text.strip(), parse_mode="HTML", reply_markup=keyboard)

@dp.message(Command("emoji_buttons"))
async def emoji_buttons_cmd(message: types.Message):
    """Test custom emoji icons on buttons"""
    
    result = await send_with_emoji_icons(
        message.chat.id,
        "Buttons with custom emoji icons (if your bot owner has Premium):"
    )
    
    if not result.get("ok"):
        await message.answer(
            f"❌ Custom emoji button icons failed.\n\n"
            f"Reason: {result.get('description')}\n\n"
            f"Note: This requires bot owner to have Telegram Premium."
        )

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
    await callback.answer(f"Clicked: {callback.data}")
    await callback.message.answer(f"✅ You selected: {callback.data}")

async def main():
    logger.info("="*60)
    logger.info("🤖 Bot Started!")
    logger.info("✅ Custom emoji in messages: ENABLED")
    logger.info("✅ Custom emoji icons on buttons: TRYING")
    logger.info("❌ Colored button backgrounds: NOT YET AVAILABLE")
    logger.info("="*60)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
