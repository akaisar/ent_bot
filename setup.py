# /setup.py file
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# dependencies
import os
import json

# from flask import Flask, request
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import deep_linking
from data.models import Quiz, MyEncoder

# bot initialization
token = os.getenv('API_BOT_TOKEN')
admin_id = int(os.getenv('OWNER_ID'))
bot = Bot(token=token)
dp = Dispatcher(bot)

quizzes = []  # здесь хранится информация о викторинах
topics = ["Physics", "Math"]


def load_data():
    with open('data.txt') as f:
        for c in json.loads(f.read()):
            for b, a in c.items():
                quizzes.append({b: Quiz(
                    quiz_id=a["quiz_id"],
                    question=a["question"],
                    options=a["options"],
                    correct_option_id=a["correct_option_id"],
                    owner_id=a["owner"]
                )})
    print("succces")


def push_data():
    with open('data.txt', 'w') as f:
        f.write(json.dumps(quizzes, cls=MyEncoder))


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    print(message.from_user)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id == admin_id:
        poll_keyboard.add(types.KeyboardButton(text="Создать викторину",
                                               request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    poll_keyboard.add(types.KeyboardButton(text="Начать тест"))
    await message.answer("Чтобы начать тестирование нажмите на кнопку ниже", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == "Начать тест")
async def choose_topic(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in topics:
        poll_keyboard.add(types.KeyboardButton(text=topic))
    await message.answer("Выберете предмет", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: topics.count(message.text) != 0)
async def start_test(message: types.Message):
    for a in quizzes:
        for topic, quiz in a.items():
            if topic != message.text:
                continue
            await bot.send_poll(chat_id=message.chat.id, question=quiz.question,
                                is_anonymous=False, options=quiz.options, type="quiz",
                                correct_option_id=quiz.correct_option_id)


@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)


@dp.message_handler(content_types=["poll"])
async def msg_with_poll(message: types.Message):
    if not message.from_user.id == admin_id:
        return
    if message.poll.type != "quiz":
        await message.reply("Извините, я принимаю только викторины (quiz)!")
        return

    # Сохраняем себе викторину в память
    question = message.poll.question
    topic = question.split()[0]
    quizzes.append({topic: Quiz(
        quiz_id=message.poll.id,
        question=' '.join(question.split()[1:]),
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=message.from_user.id)
    })
    push_data()

if __name__ == "__main__":
    load_data()
    executor.start_polling(dp, skip_updates=True)
