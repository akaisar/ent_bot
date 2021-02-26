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

quizzes_database = {}  # здесь хранится информация о викторинах
quizzes_owners = {}  # здесь хранятся пары "id викторины <--> id её создателя"
user_ans = {}  # здесь хранится количество ответов


def load_data():
    with open('data.txt') as f:
        for a in json.loads(f.read()).items():
            for b in json.loads(b).items():


def push_data():
    with open('data.txt', 'w') as f:
        f.write(json.dumps(quizzes_database, cls=MyEncoder))


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.from_user.id == admin_id:
        poll_keyboard.add(types.KeyboardButton(text="Создать викторину",
                                               request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    poll_keyboard.add(types.KeyboardButton(text="Начать тест"))
    await message.answer("Чтобы начать тестирование нажмите на кнопку ниже", reply_markup=poll_keyboard)


@dp.message_handler(lambda message: message.text == "Начать тест")
async def ent_test(message: types.Message):
    for user_id, quizzes in quizzes_database.items():
        for quiz in quizzes:
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
    # Если юзер раньше не присылал запросы, выделяем под него запись
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []

    # Если юзер решил вручную отправить не викторину, а опрос, откажем ему.
    if message.poll.type != "quiz":
        await message.reply("Извините, я принимаю только викторины (quiz)!")
        return

    # Сохраняем себе викторину в память
    quizzes_database[str(message.from_user.id)].append(Quiz(
        quiz_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=message.from_user.id)
    )
    # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
    quizzes_owners[message.poll.id] = str(message.from_user.id)
    push_data()
    await message.reply(
        f"Викторина сохранена. Общее число сохранённых викторин: {len(quizzes_database[str(message.from_user.id)])}")


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    if not user_ans.get(quiz_answer.user.id):
        user_ans[quiz_answer.user.id] = []
    for user_id, quizzes in quizzes_database.items():
        for quiz in quizzes:
            print(quiz.quiz_id, "kek")
    for saved_quiz in quizzes_database[str(quiz_answer.user.id)]:
        print(saved_quiz.quiz_id, quiz_answer.poll_id)
        if saved_quiz.quiz_id == quiz_answer.poll_id:
            if saved_quiz.correct_option_id == quiz_answer.option_ids[0]:
                user_ans[quiz_answer.user.id].append(1)
            else:
                user_ans[quiz_answer.user.id].append(0)
            if len(user_ans[quiz_answer.user.id]) == 2:
                await bot.stop_poll(saved_quiz.chat_id, saved_quiz.message_id)
    print(len(user_ans[quiz_answer.user.id]))


@dp.poll_handler(lambda active_quiz: active_quiz.is_closed is True)
async def just_poll_answer(active_quiz: types.Poll):
    quiz_owner = quizzes_owners.get(active_quiz.id)
    if not quiz_owner:
        return
    for num, saved_quiz in enumerate(quizzes_database[quiz_owner]):
        if saved_quiz.quiz_id == active_quiz.id:
            # Используем ID победителей, чтобы получить по ним имена игроков и поздравить.
            congrats_text = []
            for winner in saved_quiz.winners:
                chat_member_info = await bot.get_chat_member(saved_quiz.chat_id, winner)
                congrats_text.append(chat_member_info.user.get_mention(as_html=True))

            await bot.send_message(saved_quiz.chat_id, "Викторина закончена, всем спасибо! Вот наши победители:\n\n"
                                   + "\n".join(congrats_text), parse_mode="HTML")
            # Удаляем викторину из обоих наших "хранилищ"
            del quizzes_owners[active_quiz.id]
            del quizzes_database[quiz_owner][num]


if __name__ == "__main__":
    load_data()
    executor.start_polling(dp, skip_updates=True)
