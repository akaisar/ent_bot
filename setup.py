# /setup.py file
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# dependencies
import logging
from time import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from services import quiz_service, user_service, session_service
from config import Config
from localization.localization import Localization, Data
from utils import calc_results, ReferralStates

logging.basicConfig(level=logging.INFO)

# bot initialization
bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
user_s = user_service.UserService()
quiz_s = quiz_service.QuizService()
session_s = session_service.SessionService()
local = Localization()
quizzes_number = 3
time_between_questions = 0.75


# MARK: Send quiz

async def send_quiz(quiz, telegram_id):
    options, correct_option_id = quiz_s.shuffle_options(options=quiz.options,
                                                        correct_option_id=quiz.correct_option_id)
    msg = await bot.send_poll(chat_id=telegram_id, question=quiz.question,
                              is_anonymous=False, options=options, type="quiz",
                              correct_option_id=correct_option_id)
    sleep(time_between_questions)
    quiz_s.set_correct_option_id(quiz_id=msg.poll.id, option_id=correct_option_id)
    quiz_s.connect_ids(new_id=msg.poll.id, old_id=quiz.quiz_id)


# MARK: Send message and buttons

async def send_message_and_buttons(message, buttons, state, args=None):
    if args is None:
        args = []
    if await go_to_start(message):
        return
    if type(message) is types.Message:
        telegram_id = message.from_user.id
    else:
        telegram_id = message.user.id
    language = user_s.get_language(telegram_id=telegram_id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for index in range(0, len(buttons), 2):
        button = types.KeyboardButton(local.data[buttons[index]][language])
        if index != len(buttons) - 1:
            button2 = types.KeyboardButton(local.data[buttons[index + 1]][language])
            poll_keyboard.row(button, button2)
        else:
            poll_keyboard.add(button)
    if type(message) is types.Message:
        await message.answer(local.data[state][language].format(*args), reply_markup=poll_keyboard)
    else:
        await bot.send_message(chat_id=telegram_id, text=local.data[state][language].format(*args),
                               reply_markup=poll_keyboard)


# MARK: Send message if user not registered

async def go_to_start(message):
    if type(message) is types.Message:
        telegram_id = message.from_user.id
    else:
        telegram_id = message.user.id
    if user_s.user_exists(telegram_id=telegram_id):
        return False
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for language in local.languages:
        if type(message) is types.Message:
            await message.answer(local.data[Data.NOT_REGISTERED_MESSAGE][language], reply_markup=poll_keyboard)
        else:
            await bot.send_message(chat_id=telegram_id, text=local.data[Data.NOT_REGISTERED_MESSAGE][language],
                                   reply_markup=poll_keyboard)
    return True


# MARK: Start state

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    telegram_id = message.from_user.id
    is_new_user = await user_s.post_user(telegram_id=telegram_id)
    language = user_s.get_language(telegram_id=telegram_id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text=local.data[Data.MAIN_MENU_BUTTON][language]))
    if is_new_user:
        for language in local.languages:
            if local.languages[-1] != language:
                await message.answer(text=local.data[Data.NEW_USERS_WELCOME_MESSAGE][language])
            else:
                await message.answer(text=local.data[Data.NEW_USERS_WELCOME_MESSAGE][language],
                                     reply_markup=poll_keyboard)
    else:
        await message.answer(text=local.data[Data.WELCOME_MESSAGE][language], reply_markup=poll_keyboard)


# MARK: Set language cmd state

@dp.message_handler(commands=["language"])
async def set_language_cmd(message: types.Message):
    if await go_to_start(message):
        return
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for language in local.languages:
        poll_keyboard.add(types.KeyboardButton(text=local.data[Data.SET_LANGUAGE_BUTTON][language]))
        if local.languages[-1] != language:
            await message.answer(text=local.data[Data.SET_LANGUAGE_MESSAGE][language])
        else:
            await message.answer(text=local.data[Data.SET_LANGUAGE_MESSAGE][language], reply_markup=poll_keyboard)


# MARK: Set language result state

@dp.message_handler(lambda message: local.check_text([Data.SET_LANGUAGE_BUTTON], message.text)[0])
async def set_language_result(message: types.Message):
    if await go_to_start(message):
        return
    telegram_id = message.from_user.id
    await user_s.set_language(telegram_id=telegram_id, selected_language=message.text)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(local.data[Data.MAIN_MENU_BUTTON][message.text]))
    await message.answer(local.data[Data.MAIN_MENU_MESSAGE][message.text], reply_markup=poll_keyboard)


# MARK: Set user state cmd

@dp.message_handler(commands=["user_state"])
async def set_user_state_cmd(message: types.Message):
    await send_message_and_buttons(message=message, buttons=local.user_state_buttons, state=Data.SET_USER_STATE_MESSAGE)


# MARK: Set user state result

@dp.message_handler(lambda message: local.check_text(local.user_state_buttons, message.text)[0])
async def set_user_state_result(message: types.Message):
    if await go_to_start(message):
        return
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id=telegram_id)
    user_state = local.check_text(local.user_state_buttons, message.text)[1]
    await user_s.set_user_state(telegram_id=telegram_id, user_state=user_state)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(local.data[Data.MAIN_MENU_BUTTON][language]))
    await message.answer(local.data[Data.MAIN_MENU_MESSAGE][language], reply_markup=poll_keyboard)


# MARK: Student main menu state

@dp.message_handler(lambda message: local.check_text([Data.MAIN_MENU_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def student_main_menu(message: types.Message):
    await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                   state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Choose quiz topic state

@dp.message_handler(lambda message: local.check_text([Data.START_QUIZ_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def choose_quiz_topic(message: types.Message):
    await send_message_and_buttons(message=message, buttons=local.subjects, state=Data.CHOOSE_QUIZ_TOPIC_MESSAGE)


# MARK: Start new session

@dp.message_handler(lambda message: local.check_text(local.subjects, message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def start_new_session(message: types.Message):
    telegram_id = message.from_user.id
    topic_in_data = local.check_text(local.subjects, message.text)[1]
    topic_name = Config.DATA_SUBJECT_NAME[topic_in_data]
    user_s.user_start_new_quiz(message.from_user.id)
    quiz_ids = quiz_s.get_specified_number_of_quizzes_by_topic(topic_name=topic_name, number=quizzes_number)
    user_s.set_quiz_ids_for_user(quiz_ids=quiz_ids, telegram_id=telegram_id)
    session_s.create_session(telegram_id=telegram_id, quiz_ids=quiz_ids, topic_name=topic_name)
    await send_message_and_buttons(message=message, buttons=[Data.CANCEL_BUTTON],
                                   state=Data.START_SESSION_MESSAGE, args=[message.text, quizzes_number])
    await send_quiz(telegram_id=telegram_id, quiz=quiz_s.get_quiz_from_id(
        quiz_id=user_s.get_quiz_ids_for_user(telegram_id=message.from_user.id)))


# MARK: Cancel session

@dp.message_handler(lambda message: local.check_text([Data.CANCEL_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def cancel_session(message: types.Message):
    telegram_id = message.from_user.id
    results = user_s.get_quiz_results(telegram_id)
    session_s.post_session(telegram_id=telegram_id, results=results)
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.RESULTS_MESSAGE,
                                   args=calc_results(results=results))


# MARK: Cancel input referral
@dp.message_handler(lambda message: local.check_text([Data.CANCEL_BUTTON], text=message.text)[0],
                    state=ReferralStates.REFERRAL_STATE_0)
async def cancel_input_referral(message: types.Message):
    telegram_id = message.from_user.id
    state = dp.current_state(user=telegram_id)
    await state.finish()
    await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                   state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Input referral

@dp.message_handler(state=ReferralStates.REFERRAL_STATE_0)
async def input_referral(message: types.Message):
    telegram_id = message.from_user.id
    result = await user_s.set_student_to_teacher(telegram_id=telegram_id, referral=message.text)
    if result:
        state = dp.current_state(user=telegram_id)
        await state.finish()
        await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                       state=Data.TEACHER_ADD_SUCCESS_MESSAGE)
    else:
        await send_message_and_buttons(message, buttons=[Data.CANCEL_BUTTON], state=Data.TEACHER_ADD_UNSUCCESS_MESSAGE)


# MARK: Add student to teacher

@dp.message_handler(lambda message: local.check_text([Data.ADD_TEACHER_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def add_student_to_teacher_root(message: types.Message):
    telegram_id = message.from_user.id
    state = dp.current_state(user=telegram_id)
    await state.set_state(ReferralStates.REFERRAL_STATE_0)
    await send_message_and_buttons(message=message, buttons=[Data.CANCEL_BUTTON], state=Data.INPUT_REFERRAL_MESSAGE)


# MARK: Payment

@dp.message_handler(lambda message: local.check_text([Data.PAYMENT_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def student_payment(message: types.Message):
    await send_message_and_buttons(message=message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.STUDENT_PAYMENT_MESSAGE)


# MARK: Answer handler

@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    telegram_id = quiz_answer.user.id
    quiz_id = quiz_answer.poll_id
    is_quiz_end = user_s.user_make_answer_for_quiz(telegram_id=telegram_id,
                                                   is_option_correct=quiz_s.is_option_correct(
                                                       quiz_id=quiz_id,
                                                       option=quiz_answer.option_ids[0])
                                                   , number=quizzes_number)
    if is_quiz_end:
        results = user_s.get_quiz_results(telegram_id)
        session_s.post_session(telegram_id=telegram_id, results=results)
        await send_message_and_buttons(quiz_answer, buttons=[Data.MAIN_MENU_BUTTON], state=Data.RESULTS_MESSAGE,
                                       args=calc_results(results=results))
    else:
        await send_quiz(telegram_id=telegram_id,
                        quiz=quiz_s.get_quiz_from_id(quiz_id=user_s.get_quiz_ids_for_user(telegram_id=telegram_id)))


# MARK: Teacher Menu
@dp.message_handler(lambda message: local.check_text([Data.MAIN_MENU_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_main_menu(message: types.Message):
    await send_message_and_buttons(message, buttons=local.teacher_main_menu_buttons, state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Teacher Payment

@dp.message_handler(lambda message: local.check_text([Data.PAYMENT_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_payment(message: types.Message):
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.TEACHER_PAYMENT_MESSAGE)


# MARK: Teacher stats

@dp.message_handler(lambda message: local.check_text([Data.TEACHER_STATS_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_stats(message: types.Message):
    telegram_id = message.from_user.id
    students = await user_s.get_teacher_students(telegram_id)
    for student in students:
        await message.answer("Telegram id: "+str(student))
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.MAIN_MENU_MESSAGE)

# MARK: Default response

@dp.message_handler()
async def default_response(message: types.Message):
    if await go_to_start(message):
        return
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id=telegram_id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(local.data[Data.MAIN_MENU_BUTTON][language])
    await message.answer(local.data[Data.MAIN_MENU_MESSAGE][language], reply_markup=poll_keyboard)


if __name__ == "__main__":
    user_s.get_users()
    quiz_s.load_quizzes()
    executor.start_polling(dp, skip_updates=True)
