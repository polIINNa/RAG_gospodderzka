import os
import sys
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from RAG.rag import RAG

load_dotenv()
TOKEN = os.getenv('TELEGRAM_API_TOKEN')

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет <b>{message.from_user.first_name}</b>!\n"
                         f"Это бот, который отвечает на вопросы по документам по господдержке. Напишите вопрос - будем искать на него ответ)")


@dp.message()
async def main_handler(message: Message, bot: Bot) -> None:
    """
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    await message.answer(f'Запускаю обработку вопроса: <b>{message.text}</b>')
    if message.text is not None and message.from_user is not None:
        rag = RAG()
        response = await rag.process(query=message.text, bot=bot, user_id=message.from_user.id)
        await message.answer(f'<b>Ответ</b>:\n{response}')
    else:
        await message.answer('Не могу обработать такой формат запроса')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
