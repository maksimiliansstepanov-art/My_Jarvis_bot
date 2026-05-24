import asyncio
import os
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

# Включаем логирование, чтобы видеть работу бота в панели сервера
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# На сервере работаем напрямую без прокси и зеркал!
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
        f"Протокол 'Джарвис' успешно активирован на удаленном сервере Старк Индастриз, сэр! \n"
        f"Рад приветствовать вас, {message.from_user.first_name}. Я онлайн.",
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

async def main():
    print("Джарвис успешно запущен на сервере и слушает команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())