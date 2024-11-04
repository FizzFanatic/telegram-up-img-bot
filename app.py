import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Update
from fastapi import FastAPI, Request
import config  # Предполагается, что config.py содержит Token и WEBHOOK_URL

# Инициализация бота и диспетчера
bot = Bot(token=config.Token, parse_mode="HTML")
dp = Dispatcher()  # Dispatcher теперь инициализируется без параметров
router = Router()  # Создаем Router для регистрации хендлеров
dp.include_router(router)

# Инициализация FastAPI
app = FastAPI()

# Обработчик команды /start
@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я простой телеграм-бот.")

# Роут для вебхука
@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = await request.json()
    telegram_update = Update(**update)
    await dp.process_update(telegram_update)
    return {"ok": True}

# Установка вебхука при запуске FastAPI
@app.on_event("startup")
async def on_startup():
    # Устанавливаем вебхук для бота
    await bot.set_webhook(config.WEBHOOK_URL)

# Удаление вебхука при остановке FastAPI
@app.on_event("shutdown")
async def on_shutdown():
    # Удаляем вебхук, когда приложение выключается
    await bot.delete_webhook()

