import asyncio, os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import google.generativeai as genai
from aiohttp import web

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
user_chats = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_chats[message.chat.id] = model.start_chat(history=[])
    await message.answer("Salom! Savolingizni yuboring! ⚡")

@dp.message()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in user_chats:
        user_chats[chat_id] = model.start_chat(history=[])
    response = user_chats[chat_id].send_message(message.text)
    await message.answer(response.text)

async def handle_ping(request):
    return web.Response(text="Bot uyg'oq!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    await asyncio.gather(
        site.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
