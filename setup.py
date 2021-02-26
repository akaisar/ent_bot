# /setup.py file
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# dependencies
import os
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data.models import Quiz, MyEncoder, Student
import random

logging.basicConfig(level=logging.INFO)

# bot initialization
token = os.getenv('API_BOT_TOKEN')
admin_id = [int(i) for i in os.getenv('OWNER_ID').split()]
bot = Bot(token=token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

db_group = -1001344868552

quizzes = []  # информация о викторинах
students = []  # информация о студентах
quizzes_ids_connection = {}
current_quiz_for_user = {}  # викторины которые пользователь проходит в данный момент

topics = ["Physics", "Math"]


def load_data():
    with open('data_quizzes.txt') as f:
        data = f.read()
        if data != "":
            for c in json.loads(data):
                for b, a in c.items():
                    quizzes.append({b: Quiz(
                        quiz_id=a["quiz_id"],
                        question=a["question"],
                        options=a["options"],
                        correct_option_id=a["correct_option_id"],
                        owner_id=a["owner"]
                    )})
        else:
          logging.warning('Database is empty')

    logging.info("Bot is Up")


async def push_data():
    print("asdasd")
    with open('data_quizzes.txt', 'w') as f:
        f.write(json.dumps(quizzes, cls=MyEncoder))
    with open('data_quizzes.txt', "rb") as a:
        await bot.send_document(chat_id=db_group, document=a)


async def update_users():
    print("update users")
    with open('data_users.txt', 'w') as f:
        f.write(json.dumps(students, cls=MyEncoder))
    with open('data_users.txt', 'rb') as a:
        await bot.send_document(chat_id=db_group, document=a)
    logging.info("new question added")


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    print(message.from_user)  # TODO: Remove
    student_exists = False
    for student in students:
        if student.telegram_id == message.from_user.id:
            student_exists = True
    if not student_exists:
        students.append(
            Student(telegram_id=message.from_user.id, completed_quizzes=[])
        )
        await update_users()
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id in admin_id:
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
    current_quiz_for_user[message.from_user.id] = []
    quizzes_with_topic = []
    for a in quizzes:
        for topic, quiz in a.items():
            if topic != message.text:
                continue
            quizzes_with_topic.append(quiz)
    random.shuffle(quizzes_with_topic)
    for i in range(min(len(quizzes_with_topic), 20)):
        quiz = quizzes_with_topic[i]
        msg = await bot.send_poll(chat_id=message.chat.id, question=quiz.question,
                                  is_anonymous=False, options=quiz.options, type="quiz",
                                  correct_option_id=quiz.correct_option_id)
        quizzes_ids_connection[msg.poll.id] = quiz.quiz_id
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Начать тест"))
    await message.answer("Чтобы начать новый тест, нажмите на кнопку.", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.", reply_markup=remove_keyboard)


@dp.message_handler(content_types=["poll"])
async def msg_with_poll(message: types.Message):
    if not message.from_user.id in admin_id:
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
    await push_data()


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    quiz_id = quizzes_ids_connection[quiz_answer.poll_id]
    for student in students:
        if student.telegram_id == quiz_answer.user.id:
            student.completed_quizzes.append(quiz_answer.poll_id)
            is_answer_correct = False
            print(quiz_answer.option_ids[0])
            print("poll_id ", quiz_answer.poll_id)
            for a in quizzes:
                for topic, quiz in a.items():
                    if quiz.quiz_id == quiz_id:
                        print(quiz_id)
                        if quiz.correct_option_id == quiz_answer.option_ids[0]:
                            is_answer_correct = True
                            break
            current_quiz_for_user[student.telegram_id].append(is_answer_correct)
            if len(current_quiz_for_user[student.telegram_id]) == 2:
                correct_ans = 0
                for quiz in current_quiz_for_user[student.telegram_id]:
                    if quiz:
                        correct_ans += 1
                await bot.send_message(chat_id=student.telegram_id, text=f"Вы ответили правильно на {correct_ans} из 2")
            await update_users()


if __name__ == "__main__":
    load_data()
    executor.start_polling(dp, skip_updates=True)
