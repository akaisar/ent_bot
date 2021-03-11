# /setup.py file
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# dependencies
import logging
from time import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from services import quiz_service, user_service, session_service
from config import Config
from localization.localization import Localization
import random

logging.basicConfig(level=logging.INFO)

# bot initialization
bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
user_s = user_service.UserService()
quiz_s = quiz_service.QuizService()
session_s = session_service.SessionService()
local = Localization()
quizzes_number = 20
time_between_questions = 0.75

topics = ["Қазақ тілі", "География рус", "Қазақстан Тарихы", "История Казахстана"]


async def send_poll(quiz, telegram_id):
    options, correct_option_id = quiz_s.shuffle_options(options=quiz.options,
                                                        correct_option_id=quiz.correct_option_id)
    msg = await bot.send_poll(chat_id=telegram_id, question=quiz.question,
                              is_anonymous=False, options=options, type="quiz",
                              correct_option_id=correct_option_id)
    sleep(time_between_questions)
    quiz_s.post_correct_option_id(quiz_id=msg.poll.id, option_id=correct_option_id)
    quiz_s.connect_ids(new_id=msg.poll.id, old_id=quiz.quiz_id)


@dp.message_handler(commands=["start", "language"])
async def cmd_start(message: types.Message):
    logging.info(message.from_user)
    await user_s.post_user(telegram_id=message.from_user.id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # if message.from_user.id in Config.ADMIN_IDS:
    #     poll_keyboard.add(types.KeyboardButton(text="Создать викторину",
    #                                            request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    poll_keyboard.row(types.KeyboardButton(text="Қазақ"), types.KeyboardButton(text="Русский"))
    await message.answer("Тіл танданыз, Выберите язык", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: local.check_text(["languages"], message.text))
async def start_app(message: types.Message):
    await user_s.post_user(telegram_id=message.from_user.id)
    await user_s.set_user_language(telegram_id=message.from_user.id, selected_language=message.text)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text=local.get_text(text="start button",
                                                               telegram_id=message.from_user.id,
                                                               user_s=user_s)))
    await message.answer(local.get_text(text="start message", telegram_id=message.from_user.id, user_s=user_s),
                         reply_markup=poll_keyboard)


@dp.message_handler(lambda message: local.check_text(["start button"], message.text))
async def choose_topic(message: types.Message):
    await user_s.post_user(telegram_id=message.from_user.id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for index in range(len(topics)):
        if index % 2 == 0:
            if index != len(topics):
                poll_keyboard.row(types.KeyboardButton(text=local.get_text(text=topics[index], user_s=user_s,
                                                                           telegram_id=message.from_user.id)),
                                  types.KeyboardButton(text=local.get_text(text=topics[index+1], user_s=user_s,
                                                                           telegram_id=message.from_user.id))                                  )
            else:
                poll_keyboard.row(types.KeyboardButton(text=local.get_text(text=topics[index], user_s=user_s,
                                                                           telegram_id=message.from_user.id)))
    await message.answer(local.get_text(text="select message", telegram_id=message.from_user.id,
                                        user_s=user_s), reply_markup=poll_keyboard)


@dp.message_handler(lambda message: local.check_text(texts=local.subjects, message=message.text))
async def start_test(message: types.Message):
    await user_s.post_user(telegram_id=message.from_user.id)
    key_text = local.get_key(text=message.text)
    user_s.user_start_new_quiz(message.from_user.id)
    quiz_ids = quiz_s.load_few_quizzes_from_topic(topic_name=key_text, number=quizzes_number)
    user_s.set_quiz_ids_for_user(quiz_ids=quiz_ids, telegram_id=message.from_user.id)
    session_s.create_session(telegram_id=message.from_user.id, quiz_ids=quiz_ids, topic_name=key_text)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text=local.get_text(text="start button",
                                                               telegram_id=message.from_user.id,
                                                               user_s=user_s)))
    await message.answer(local.get_text(text="quiz number message", user_s=user_s, telegram_id=message.from_user.id)
                         .format(quizzes_number), reply_markup=poll_keyboard)
    await send_poll(telegram_id=message.chat.id,
                    quiz=quiz_s.get_quiz_from_id(quiz_id=user_s.get_quiz_ids_for_user(telegram_id=message.from_user.id)))


# @dp.message_handler(content_types=["poll"])
# async def msg_with_poll(message: types.Message):
#     if message.from_user.id not in Config.ADMIN_IDS:
#         return
#     if message.poll.type != "quiz":
#         await message.reply("Извините, я принимаю только викторины (quiz)!")
#         return
#     question = message.poll.question
#     try:
#         r = quiz_s.push_quiz_to_api(topic=question.split()[0], quiz_id=message.poll.id,
#                                     question=' '.join(question.split()[1:]),
#                                     options=[o.text for o in message.poll.options],
#                                     correct_option_id=message.poll.correct_option_id,
#                                     owner_id=message.from_user.id)
#         await message.answer(r)
#     except Exception as e:
#         print(e)
#         logging.info("can't reach api, question upload failed will continue with next poll creation")


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    await user_s.post_user(telegram_id=quiz_answer.user.id)
    quiz_id = quiz_s.get_old_id(quiz_answer.poll_id)
    await user_s.complete_quiz(quiz_id=quiz_id, telegram_id=quiz_answer.user.id)
    data = user_s.user_make_answer_for_quiz(telegram_id=quiz_answer.user.id,
                                            is_option_correct=quiz_s.is_option_correct(quiz_id=quiz_answer.poll_id,
                                                                                       option=quiz_answer.option_ids[0])
                                            , number=quizzes_number)
    if data[0]:
        poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        session_s.post_session(telegram_id=quiz_answer.user.id, results=user_s.get_quiz_results(
            telegram_id=quiz_answer.user.id))
        poll_keyboard.add(types.KeyboardButton(text=local.get_text(text="start button",
                                                                   telegram_id=quiz_answer.user.id,
                                                                   user_s=user_s)))
        await bot.send_message(chat_id=quiz_answer.user.id,
                               text=local.get_text(text="result message",
                                                   telegram_id=quiz_answer.user.id,
                                                   user_s=user_s).format(data[1], quizzes_number))
        await bot.send_message(chat_id=quiz_answer.user.id,
                               text=local.get_text(text="restart message",
                                                   telegram_id=quiz_answer.user.id,
                                                   user_s=user_s), reply_markup=poll_keyboard)
    else:
        await send_poll(telegram_id=quiz_answer.user.id,
                        quiz=quiz_s.get_quiz_from_id(
                            quiz_id=user_s.get_quiz_ids_for_user(telegram_id=quiz_answer.user.id)))


if __name__ == "__main__":
    user_s.get_users()
    executor.start_polling(dp, skip_updates=True)
