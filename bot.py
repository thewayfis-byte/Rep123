import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# Вставь сюда свой токен от @BotFather
TOKEN = "8849183810:AAEUxypEjlUmTm5RAvaEX6UsuTg0-88JjDQ"
# Когда запустишь ngrok, вставь сюда полученную https ссылку
APP_URL = "https://your-ngrok-url.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Играть в Flappy Bird 🐦", 
        web_app=WebAppInfo(url=APP_URL)
    ))
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! Нажми на кнопку ниже:",
        reply_markup=builder.as_markup()
    )

# Настройка раздачи статических файлов
async def handle_index(request):
    return web.FileResponse('./index.html')

async def main():
    # Создаем веб-приложение aiohttp
    app = web.Application()
    app.router.add_get('/', handle_index)
    # Важно: статика должна быть после конкретных маршрутов
    app.router.add_static('/', path='./')
    
    # Настройка запуска сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    print("Сайт запущен на http://localhost:8080")
    print("Бот запущен...")
    
    # Запуск бота
    try:
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
