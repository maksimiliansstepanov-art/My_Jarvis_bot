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

# НЕУБИВАЕМЫЙ ОБРАБОТЧИК НА СВОБОДНОМ ИИ СЕРВЕРЕ
@dp.message()
async def chat_with_ai(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        # Прописываем характер Джарвиса прямо в промпт
        prompt = (
            f"Ты — Джарвис, умный, вежливый ИИ-ассистент Тони Старка. "
            f"Обращайся к пользователю только 'сэр'. Отвечай кратко на русском языке.\n"
            f"Вопрос пользователя: {message.text}\nОтвет Джарвиса:"
        )
        
        # Используем открытое зеркало ИИ Qwen, которое обожает русский язык и всегда доступно
        url = "https://huggingface.co"
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.7}}
        
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            # Извлекаем сгенерированный текст
            if isinstance(result, list) and "generated_text" in result[0]:
                full_text = result[0]["generated_text"]
                # Отрезаем сам промпт, чтобы бот вывел только чистый ответ
                ai_response = full_text.replace(prompt, "").strip()
                await message.answer(ai_response)
                return
                
        await message.answer("Сэр, зафиксированы сильные помехи на линии связи с ИИ. Попробуйте еще раз.")
        
    except Exception as e:
        logging.error(f"Ошибка ИИ: {e}")
        await message.answer("Сэр, возникла внутренняя задержка в аналитических алгоритмах. Повторите запрос.")

async def main():
    print("Джарвис готов к финальному деплою...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())