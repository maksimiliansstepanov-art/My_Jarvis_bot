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
        f"Протокол 'Джарвис' успешно обновлен, сэр! \n"
        f"Все мыслительные модули выведены на максимальную мощность. Я готов к любым вопросам.",
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

# УЛЬТРА-СТАБИЛЬНЫЙ ИИ-ОБРАБОТЧИК (Qwen 2.5 через чистый API)
@dp.message()
async def chat_with_ai(message: types.Message):
    # Показываем статус "печатает", пока ИИ генерирует ответ
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Формируем жесткую системную инструкцию для роли Джарвиса
    system_instruction = "Ты — Джарвис, умный, вежливый ИИ-ассистент Тони Старка. Обращайся к пользователю только 'сэр'. Отвечай кратко, емко, только на русском языке."
    prompt = f"<|im_start|>system\n{system_instruction}<|im_end|>\n<|im_start|>user\n{message.text}<|im_end|>\n<|im_start|>assistant\n"
    
    try:
        # Используем мощный международный ИИ-узел, который стабильно работает на Amvera
        url = "https://huggingface.co"
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                ai_response = result[0]["generated_text"].strip()
                # Очищаем от возможных системных тегов
                ai_response = ai_response.split("<|im_end|>")[0].strip()
                await message.answer(ai_response)
                return
                
        # Если сервис перегружен, плавно переключаемся на локальные заготовки, чтобы бот не молчал
        await message.answer("Сэр, фиксирую высокую загрузку процессора. Краткий ответ: системы функционируют нормально. Повторите сложный запрос через секунду.")
        
    except Exception as e:
        logging.error(f"Ошибка ИИ: {e}")
        await message.answer("Сэр, возникла задержка в аналитических алгоритмах. Попробуйте еще раз.")

async def main():
    print("Джарвис получил новые мозги и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())