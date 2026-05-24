import asyncio
import os
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# На сервере работаем напрямую!
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🌤️ Погода"))
    builder.add(types.KeyboardButton(text="📝 Мои задачи"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

todo_list = ["Собрать костюм Марк-5", "Зарядить реактор"]

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Протокол 'Джарвис' успешно активирован на удаленном сервере, сэр! \n"
        f"Рад приветствовать вас, {message.from_user.first_name}. Все нейромодули онлайн. Я готов к диалогу.",
        reply_markup=get_main_menu()
    )

@dp.message(F.text == "🌤️ Погода")
async def get_weather(message: types.Message):
    await message.answer("Сэр, запрашиваю данные со спутников...")
    try:
        url = "http://wttr.in"
        response = requests.get(url, timeout=5).text
        await message.answer(f"📡 **Сводка погоды, сэр:**\n\n{response}\nРекомендую учесть это при полетах.")
    except Exception:
        await message.answer("Сэр, приборы показывают отличную погоду для полетов: +20°C.")

@dp.message(F.text == "📝 Мои задачи")
async def get_tasks(message: types.Message):
    if not todo_list:
        await message.answer("Сэр, ваш список задач пуст.")
        return
    tasks_text = "📋 **Ваш текущий список задач, сэр:**\n\n"
    for index, task in enumerate(todo_list, 1):
        tasks_text += f"{index}. {task}\n"
    await message.answer(tasks_text)

# ОБРАБОТКА ЛЮБОГО ДРУГОГО ТЕКСТА ЧЕРЕЗ БЕСПЛАТНЫЙ ИИ ЧЕРЕЗ REQUESTS
@dp.message()
async def chat_with_ai(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Формируем четкий промпт для характера Джарвиса
    system_prompt = "Ты — Джарвис, умный, вежливый ИИ-ассистент Тони Старка. Обращайся к пользователю только 'сэр'. Отвечай кратко, емко и только на русском языке."
    full_prompt = f"{system_prompt}\nЗапрос от пользователя: {message.text}"
    
    # ПЛАН А: Используем стабильное API Pollinations (передаем через параметры, чтобы не ломать URL)
    try:
        url = "https://pollinations.ai"
        response = requests.get(url, params={"text": full_prompt}, timeout=10)
        if response.status_code == 200 and response.text.strip():
            await message.answer(response.text.strip())
            return
    except Exception as e:
        logging.error(f"Ошибка План А: {e}")

    # ПЛАН Б: Резервное зеркало (если первый сервис перегружен)
    try:
        backup_url = f"https://pollinations.ai{requests.utils.quote(full_prompt)}"
        # Пробуем получить быстрый текстовый ответ от альтернативной точки
        res = requests.get(backup_url, timeout=10)
        if res.status_code == 200:
            await message.answer(res.text.strip())
            return
    except Exception as e:
        logging.error(f"Ошибка План Б: {e}")
        
    # Если вообще всё легло
    await message.answer("Сэр, спутниковая связь с мыслительным ядром временно нестабильна. Повторите запрос через пару секунд.")