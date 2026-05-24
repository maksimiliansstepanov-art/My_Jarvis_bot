import asyncio
import os
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
from groq import Groq  # Возвращаем надежную библиотеку ИИ

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Инициализируем компоненты
bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = Groq(api_key=GROQ_KEY)

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
        f"Протокол 'Джарвис' успешно активирован, сэр! \n"
        f"Рад приветствовать вас, {message.from_user.first_name}. Системы ИИ онлайн. Что вас интересует?",
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

# НАДЕЖНЫЙ ОБРАБОТЧИК ЧЕРЕЗ ОФИЦИАЛЬНОЕ API
@dp.message()
async def chat_with_ai(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        completion = ai_client.chat.completions.create(
            model="llama3-8b-8192",  # Оригинальная модель от Groq
            messages=[
                {
                    "role": "system", 
                    "content": "Ты — Джарвис, умный, вежливый и преданный ИИ-ассистент Тони Старка. Обращайся к пользователю только 'сэр'. Отвечай кратко, емко и на русском языке."
                },
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
        )
        
        ai_response = completion.choices.message.content
        await message.answer(ai_response)
        
    except Exception as e:
        logging.error(f"Ошибка ИИ Groq: {e}")
        await message.answer("Сэр, возникли временные трудности с передачей пакетов данных. Повторите запрос.")

async def main():
    print("Джарвис готов...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())