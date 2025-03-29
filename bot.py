import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ChatType

import os

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


# Хранилище сообщений
user_messages = {}

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Обработка личных сообщений от пользователей
@dp.message(F.chat.type == ChatType.PRIVATE)
async def handle_user_message(message: Message):
    user_id = message.from_user.id
    user_messages[user_id] = message

    text = f"Новое сообщение от @{message.from_user.username or 'без юзернейма'}:\n{message.text}"
    await bot.send_message(ADMIN_ID, text)
    await message.reply("Спасибо за сообщение! Я скоро отвечу.")


# Ответ администратора
@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def handle_admin_reply(message: Message):
    for user_id, original_message in user_messages.items():
        if original_message.text in message.reply_to_message.text:
            await bot.send_message(user_id, f"Ответ администратора:\n{message.text}")
            break


# Главная функция запуска
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

