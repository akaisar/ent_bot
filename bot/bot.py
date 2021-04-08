import logging
import re
import threading
import asyncio
from time import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook
from services import quiz_service, user_service, session_service, subject_service
from config import Config
from localization.localization import Localization, Data
from utils import calc_results, ReferralStates, UserNameStates, TeacherStatStates, SynopsesStates, SessionStates, \
    SubjectsStates

logging.basicConfig(level=logging.INFO)
# bot initialization
bot = Bot(token=Config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
user_s = user_service.UserService()
quiz_s = quiz_service.QuizService()
session_s = session_service.SessionService()
subject_s = subject_service.SubjectService()
local = Localization()

def load_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(user_s.get_users())
    loop.run_until_complete(quiz_s.load_quizzes())
    loop.run_until_complete(subject_s.load_subjects())


async def on_startup(dp):
    await bot.set_webhook(Config.WEBHOOK_URL, drop_pending_updates=True)
    logging.warning(
        'Starting connection. ')


def main():
    x = threading.Thread(target=load_db)
    x.start()
    start_webhook(
        dispatcher=dp,
        webhook_path=Config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=Config.WEBAPP_HOST,
        port=Config.WEBAPP_PORT,
    )


if __name__ == "__main__":
    load_db()
    executor.start_polling(dp, skip_updates=True)
