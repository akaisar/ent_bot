# /setup.py file
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# dependencies
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
time_between_questions = 0.75


# MARK: Send students like button

async def send_students_like_button(message, state):
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id)
    students = user_s.get_teacher_students(telegram_id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(local.data[Data.CANCEL_BUTTON][language])
    language = user_s.get_language(telegram_id=telegram_id)
    for index in range(len(students)):
        student_id = students[index]
        name = user_s.get_name(student_id)
        poll_keyboard.add(str(index) + ") " + name)
    await message.answer(local.data[state][language], reply_markup=poll_keyboard)


# MARK: Send student stats

async def send_student_stats(message, telegram_id, stats, language, index=None):
    name = user_s.get_name(telegram_id)
    args = [name, stats["correct_all_time"], stats["correct_all_time"] + stats["incorrect_all_time"],
            stats["Last_7_days_correct_question_number:"], stats["Last_7_days_question_number:"],
            stats["Profile_creation_date"]]
    if index is not None:
        base_stats = f"№ {index}\n" + local.data[Data.STUDENT_STATS_MESSAGE][language].format(*args)
    else:
        base_stats = local.data[Data.STUDENT_STATS_MESSAGE][language].format(*args)
    other_stats = [local.data[Data.SUBJECT_INFO_FORMAT_MESSAGE][language]]
    for subject in local.subjects:
        subject_name = Config.DATA_SUBJECT_NAME[subject]
        if subject_name in stats:
            other_stats.append(f"{local.data[subject][language]} / {stats[subject_name]} / "
                               f"{stats[subject_name + '_correct']}")
    await message.answer(base_stats + "\n".join(other_stats))


# MARK: Send quiz

async def send_quiz(quiz, telegram_id, is_poll, quizzes_number):
    if quiz_s.is_in_quiz_set(quiz.quiz_id):
        if user_s.is_send_text(telegram_id):
            msg = await bot.send_message(chat_id=telegram_id, text=quiz_s.get_quiz_set_text(quiz.quiz_id))
    quiz_number = len(user_s.quiz_results[telegram_id]) + 1
    if quiz.is_image:
        with open(f"data/images/{Config.DATA_SUBJECT_NAME[quiz.topic]}/{quiz.question}.png", 'rb') as f:
            photo = f
            await bot.send_photo(chat_id=telegram_id, photo=photo)
        options = local.options[:int(quiz.options[0])]
        correct_option_ids = quiz.correct_option_ids
        if is_poll:
            allows_multiple_answers = len(options) > 5
            msg = await bot.send_poll(chat_id=telegram_id, question=f"[{quiz_number}:{quizzes_number}]",
                                      is_anonymous=False, options=options,
                                      allows_multiple_answers=allows_multiple_answers)
        else:
            msg = await bot.send_poll(chat_id=telegram_id, question=f"[{quiz_number}:{quizzes_number}]",
                                      is_anonymous=False, options=options, type="quiz",
                                      correct_option_id=correct_option_ids[0])
    else:
        options, correct_option_ids = quiz_s.shuffle_options(options=quiz.options,
                                                             correct_option_ids=quiz.correct_option_ids)
        is_options_correct = True
        for option in options:
            if len(option) > 100:
                is_options_correct = False
        if len(quiz.question) <= 300 and is_options_correct:
            if is_poll:
                allows_multiple_answers = len(options) > 5
                msg = await bot.send_poll(chat_id=telegram_id,
                                          question=f"[{quiz_number}:{quizzes_number}]\n" + quiz.question,
                                          is_anonymous=False, options=options,
                                          allows_multiple_answers=allows_multiple_answers)
            else:
                msg = await bot.send_poll(chat_id=telegram_id,
                                          question=f"[{quiz_number}:{quizzes_number}]\n" + quiz.question,
                                          is_anonymous=False, options=options, type="quiz",
                                          correct_option_id=correct_option_ids[0])
        else:
            text = f"[{quiz_number}:{quizzes_number}]\n" + quiz.question + "\n"
            options2 = local.options[:len(options)]
            for index in range(len(options)):
                option = options[index]
                text += options2[index] + " " + option
                if text[-1] != "\n":
                    text += "\n"
            await bot.send_message(chat_id=telegram_id, text=text)
            if is_poll:
                allows_multiple_answers = len(options) > 5
                msg = await bot.send_poll(chat_id=telegram_id, question=" ",
                                          is_anonymous=False, options=options2,
                                          allows_multiple_answers=allows_multiple_answers)
            else:
                msg = await bot.send_poll(chat_id=telegram_id, question=" ",
                                          is_anonymous=False, options=options2, type="quiz",
                                          correct_option_id=correct_option_ids[0])
    sleep(time_between_questions)
    quiz_s.set_correct_option_ids(quiz_id=msg.poll.id, option_ids=correct_option_ids)
    quiz_s.connect_ids(new_id=msg.poll.id, old_id=quiz.quiz_id)


def get_poll_keyboard(buttons):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for index in range(0, len(buttons), 2):
        if index != len(buttons) - 1:
            poll_keyboard.row(buttons[index], buttons[index + 1])
        else:
            poll_keyboard.add(buttons[index])
    return poll_keyboard


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

@dp.message_handler(lambda message: local.check_text([Data.LANGUAGE_BUTTON], message.text)[0] or
                                    message.text == "/language")
async def set_language_cmd(message: types.Message):
    if await go_to_start(message):
        return
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for language in local.languages:
        poll_keyboard.add(types.KeyboardButton(text=local.data[language][language]))
        if local.languages[-1] != language:
            await message.answer(text=local.data[Data.SET_LANGUAGE_MESSAGE][language])
        else:
            await message.answer(text=local.data[Data.SET_LANGUAGE_MESSAGE][language], reply_markup=poll_keyboard)


# MARK: Set language result state

@dp.message_handler(lambda message: local.check_text(local.languages, message.text)[0])
async def set_language_result(message: types.Message):
    if await go_to_start(message):
        return
    telegram_id = message.from_user.id
    language = local.check_text(local.languages, message.text)[1]
    await user_s.set_language(telegram_id=telegram_id, selected_language=language)
    profile_info = user_s.get_user_profile(telegram_id=telegram_id, user_language=language)
    await send_message_and_buttons(message=message, buttons=local.profile, state=Data.PROFILE_MESSAGE,
                                   args=[profile_info])


# MARK: Set user state cmd

@dp.message_handler(lambda message: local.check_text([Data.USER_STATE_BUTTON], text=message.text)[0] or
                                    message.text == "/user_state")
async def set_user_state_cmd(message: types.Message):
    await send_message_and_buttons(message=message, buttons=local.user_state_buttons, state=Data.SET_USER_STATE_MESSAGE)


# MARK: Set user state result

@dp.message_handler(lambda message: local.check_text(local.user_state_buttons, message.text)[0])
async def set_user_state_result(message: types.Message):
    if await go_to_start(message):
        return
    telegram_id = message.from_user.id
    user_state = local.check_text(local.user_state_buttons, message.text)[1]
    await user_s.set_user_state(telegram_id=telegram_id, user_state=user_state)
    language = user_s.get_language(telegram_id)
    profile_info = user_s.get_user_profile(telegram_id=telegram_id, user_language=language)
    await send_message_and_buttons(message=message, buttons=local.profile, state=Data.PROFILE_MESSAGE,
                                   args=[profile_info])


# MARK: Cancel set profile

@dp.message_handler(lambda message: local.check_text([Data.CANCEL_BUTTON], message.text)[0],
                    state=SubjectsStates.all_states + UserNameStates.all_states)
async def cancel_set_profile(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.finish()
    language = user_s.get_language(telegram_id)
    profile_info = user_s.get_user_profile(telegram_id=telegram_id, user_language=language)
    await send_message_and_buttons(message=message, buttons=local.profile, state=Data.PROFILE_MESSAGE,
                                   args=[profile_info])


# MARK: Set user name result

@dp.message_handler(state=UserNameStates.USER_NAME_STATE_0)
async def set_user_name_result(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.finish()
    await user_s.set_user_name(telegram_id=message.from_user.id, name=message.text)
    language = user_s.get_language(telegram_id)
    profile_info = user_s.get_user_profile(telegram_id=telegram_id, user_language=language)
    await send_message_and_buttons(message=message, buttons=local.profile, state=Data.PROFILE_MESSAGE,
                                   args=[profile_info])


# MARK: Set user name

@dp.message_handler(lambda message: local.check_text([Data.USER_NAME_BUTTON], message.text)[0])
async def set_user_name(message: types.Message):
    if await go_to_start(message):
        return
    telegram_id = message.from_user.id
    state = dp.current_state(user=telegram_id)
    await state.set_state(UserNameStates.USER_NAME_STATE_0)
    await send_message_and_buttons(message=message, buttons=[Data.CANCEL_BUTTON], state=Data.INPUT_NAME_MESSAGE)


# MARK: Start ent

@dp.message_handler(lambda message: local.check_text([Data.ENT_BUTTON], message.text)[0])
async def start_ent(message: types.Message):
    telegram_id = message.from_user.id
    subject_1, subject_2 = user_s.get_student_subjects(telegram_id)
    user_s.user_start_new_quiz(telegram_id)
    user_s.set_quiz_type(telegram_id, True)
    quiz_sets = quiz_s.get_quiz_sets(topic=Data.READING_LITERACY_RUS, quiz_number=15)
    user_s.set_quiz_sets(telegram_id=telegram_id, quiz_sets=quiz_sets)
    quiz_ids_reading = quiz_s.quiz_set_to_quiz_ids(quiz_sets, 20)
    quiz_ids_history = quiz_s.get_specified_number_of_quizzes_by_topic(topic_name=Data.KAZ_HISTORY_RUS, number=15)
    quiz_ids_math = quiz_s.get_specified_number_of_quizzes_by_topic(topic_name=Data.MATH_LITERACY_RUS, number=15)
    quiz_ids_subject_1 = quiz_s.get_specified_number_of_quizzes_by_topic(topic_name=subject_1, number=20)
    quiz_ids_subject_2 = quiz_s.get_specified_number_of_quizzes_by_topic(topic_name=subject_2, number=20)
    print(quiz_ids_math)
    print(len(quiz_ids_math))
    quiz_ids = quiz_ids_history + quiz_ids_math + quiz_ids_reading + quiz_ids_subject_1 + \
               quiz_ids_subject_2
    quizzes_number = len(quiz_ids)
    user_s.set_quiz_size(telegram_id, quizzes_number)
    user_s.set_quiz_ids_for_user(quiz_ids=quiz_ids, telegram_id=telegram_id)
    session_s.create_session(telegram_id=telegram_id, quiz_ids=quiz_ids, topic_name=Data.ENT)
    await send_message_and_buttons(message=message, buttons=[Data.CANCEL_BUTTON],
                                   state=Data.START_SESSION_MESSAGE, args=[message.text, quizzes_number])
    await send_quiz(telegram_id=telegram_id, quiz=quiz_s.get_quiz_from_id(
        quiz_id=user_s.get_quiz_ids_for_user(telegram_id=message.from_user.id)), is_poll=True,
                    quizzes_number=quizzes_number)


# MARK: Student main menu state


@dp.message_handler(lambda message: local.check_text([Data.MAIN_MENU_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def student_main_menu(message: types.Message):
    await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                   state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Student synopses return to main menu

@dp.message_handler(lambda message: local.check_text([Data.MAIN_MENU_BUTTON], message.text)[0],
                    state=SynopsesStates.SYNOPSES_STATE_0)
async def student_synopses_return_to_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                   state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Student synopses subtopic text
@dp.message_handler(lambda message: subject_s.is_subtopic_name(message.text) and user_s.is_student(telegram_id=
                                                                                                   message.from_user.id))
async def student_synopses_subtopic_text(message: types.Message):
    telegram_id = message.from_user.id
    text = subject_s.get_subtopic_text(message.text)
    print(text)
    await bot.send_message(chat_id=telegram_id, text=text)
    await send_message_and_buttons(message=message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.MAIN_MENU_MESSAGE)


# MARK: Student synopses choose subject

@dp.message_handler(lambda message: local.check_text(local.synopses_subjects, message.text)[0],
                    state=SynopsesStates.SYNOPSES_STATE_0)
async def student_synopses_choose_subject(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id)
    await state.finish()
    subtopics = subject_s.get_subject_topics(topic_name=local.check_text(local.synopses_subjects, message.text)[1])
    poll_keyboard = get_poll_keyboard(subtopics)
    poll_keyboard.add(local.data[Data.MAIN_MENU_BUTTON][language])
    await message.answer(local.data[Data.CHOOSE_SUBTOPIC_MESSAGE][language], reply_markup=poll_keyboard)


# MARK: Student synopses state

@dp.message_handler(lambda message: local.check_text([Data.SYNOPSES_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def student_synopses(message: types.Message, state: FSMContext):
    await state.set_state(SynopsesStates.SYNOPSES_STATE_0)
    await send_message_and_buttons(message=message, buttons=local.synopses_subjects, state=Data.CHOOSE_TOPIC_MESSAGE)


# MARK: Choose quiz topic state

@dp.message_handler(lambda message: local.check_text([Data.START_QUIZ_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def choose_quiz_topic(message: types.Message, state: FSMContext):
    await state.set_state(SessionStates.SESSION_STATE_0)
    await send_message_and_buttons(message=message, buttons=local.subjects, state=Data.CHOOSE_TOPIC_MESSAGE)


# MARK: Start session

@dp.message_handler(lambda message: local.check_text(local.subjects, message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id),
                    state=SessionStates.SESSION_STATE_0)
async def start_new_session(message: types.Message, state: FSMContext):
    quizzes_number = 20
    await state.finish()
    telegram_id = message.from_user.id
    topic_name = local.check_text(local.subjects, message.text)[1]
    user_s.set_quiz_size(telegram_id, quizzes_number)
    user_s.user_start_new_quiz(message.from_user.id)
    user_s.set_quiz_type(telegram_id, False)
    quiz_ids = quiz_s.get_specified_number_of_quizzes_by_topic(topic_name=topic_name, number=quizzes_number)
    user_s.set_quiz_ids_for_user(quiz_ids=quiz_ids, telegram_id=telegram_id)
    session_s.create_session(telegram_id=telegram_id, quiz_ids=quiz_ids, topic_name=topic_name)
    await send_message_and_buttons(message=message, buttons=[Data.CANCEL_BUTTON],
                                   state=Data.START_SESSION_MESSAGE, args=[message.text, quizzes_number])
    await send_quiz(telegram_id=telegram_id, quiz=quiz_s.get_quiz_from_id(
        quiz_id=user_s.get_quiz_ids_for_user(telegram_id=message.from_user.id)), is_poll=False,
                    quizzes_number=quizzes_number)


# MARK: Cancel session

@dp.message_handler(lambda message: local.check_text([Data.CANCEL_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def cancel_session(message: types.Message):
    telegram_id = message.from_user.id
    results = user_s.get_quiz_results(telegram_id)
    await session_s.post_session(telegram_id=telegram_id, results=results)
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.RESULTS_MESSAGE,
                                   args=calc_results(results=results))


# MARK: Cancel input referral
@dp.message_handler(lambda message: local.check_text([Data.CANCEL_BUTTON], text=message.text)[0],
                    state=ReferralStates.REFERRAL_STATE_0)
async def cancel_input_referral(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.finish()
    await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                   state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Input referral

@dp.message_handler(state=ReferralStates.REFERRAL_STATE_0)
async def input_referral(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    result = await user_s.set_student_to_teacher(telegram_id=telegram_id, referral=message.text)
    if result:
        await state.finish()
        await send_message_and_buttons(message=message, buttons=local.student_main_menu_buttons,
                                       state=Data.TEACHER_ADD_SUCCESS_MESSAGE)
    else:
        await send_message_and_buttons(message, buttons=[Data.CANCEL_BUTTON], state=Data.TEACHER_ADD_UN_SUCCESS_MESSAGE)


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


# MARK: Student stats

@dp.message_handler(lambda message: local.check_text([Data.STUDENT_STATS_BUTTON], message.text)[0] and
                                    user_s.is_student(telegram_id=message.from_user.id))
async def student_stats(message: types.Message):
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id)
    stats = await user_s.get_student_stats(telegram_id)
    await send_student_stats(message=message, telegram_id=telegram_id, stats=stats, language=language)


# MARK: Answer handler

@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    telegram_id = quiz_answer.user.id
    if not session_s.have_active_session(telegram_id):
        return
    quiz_id = quiz_answer.poll_id
    is_quiz_end = user_s.user_make_answer_for_quiz(telegram_id=telegram_id,
                                                   is_option_correct=quiz_s.is_option_correct(
                                                       quiz_id=quiz_id,
                                                       option=quiz_answer.option_ids[0])
                                                   , number=user_s.get_quiz_size(telegram_id))
    if is_quiz_end:
        results = user_s.get_quiz_results(telegram_id)
        await session_s.post_session(telegram_id=telegram_id, results=results)
        await send_message_and_buttons(quiz_answer, buttons=[Data.MAIN_MENU_BUTTON], state=Data.RESULTS_MESSAGE,
                                       args=calc_results(results=results))
    else:
        await send_quiz(telegram_id=telegram_id,
                        quiz=quiz_s.get_quiz_from_id(quiz_id=user_s.get_quiz_ids_for_user(telegram_id=telegram_id)),
                        is_poll=user_s.get_quiz_type(telegram_id), quizzes_number=user_s.get_quiz_size(telegram_id))


# MARK: Teacher Menu
@dp.message_handler(lambda message: local.check_text([Data.MAIN_MENU_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_main_menu(message: types.Message):
    await send_message_and_buttons(message, buttons=local.teacher_main_menu_buttons, state=Data.IN_MAIN_MENU_MESSAGE)


# MARK: Teacher payment

@dp.message_handler(lambda message: local.check_text([Data.PAYMENT_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_payment(message: types.Message):
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.TEACHER_PAYMENT_MESSAGE)


# MARK: Teacher stats

@dp.message_handler(lambda message: local.check_text([Data.TEACHER_STATS_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_stats(message: types.Message):
    telegram_id = message.from_user.id
    students = user_s.get_teacher_students(telegram_id)
    language = user_s.get_language(telegram_id)
    for index in range(len(students)):
        student_id = students[index]
        stats = await user_s.get_student_stats(student_id)
        await send_student_stats(message=message, telegram_id=student_id, stats=stats, language=language, index=index)
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON, Data.DELETE_STUDENT_FROM_TEACHER_BUTTON],
                                   state=Data.MAIN_MENU_MESSAGE)


# MARK: Delete student from teacher

@dp.message_handler(lambda message: local.check_text([Data.DELETE_STUDENT_FROM_TEACHER_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def delete_student_from_teacher(message: types.Message, state: FSMContext):
    await send_students_like_button(message, state=Data.DELETE_STUDENT_FROM_TEACHER_MESSAGE)
    await state.set_state(TeacherStatStates.TEACHER_STAT_STATE_0)


# MARK: Delete student from teacher cancel

@dp.message_handler(lambda message: local.check_text([Data.CANCEL_BUTTON], text=message.text)[0],
                    state=TeacherStatStates.TEACHER_STAT_STATE_0)
async def delete_student_from_teacher_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await send_message_and_buttons(message, buttons=local.teacher_main_menu_buttons,
                                   state=Data.MAIN_MENU_MESSAGE)


# MARK: Delete student from teacher result

@dp.message_handler(state=TeacherStatStates.TEACHER_STAT_STATE_0)
async def delete_student_from_teacher_result(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id)
    nums = re.findall(r"\d+", message.text)
    student_pos = -1
    if len(nums) > 0:
        student_pos = nums[0]
    if student_pos != -1:
        is_correct = await user_s.delete_student_from_teacher(teacher_id=telegram_id, student_pos=student_pos)
        if is_correct:
            await state.finish()
            await send_message_and_buttons(message, buttons=local.teacher_main_menu_buttons,
                                           state=Data.TEACHER_DELETE_STUDENT_SUCCESS_MESSAGE)
            return
    await send_students_like_button(message, state=Data.TEACHER_DELETE_STUDENT_UN_SUCCESS_MESSAGE)


# MARK: About us

@dp.message_handler(lambda message: local.check_text([Data.ABOUT_US_BUTTON], text=message.text)[0])
async def about_us(message: types.Message):
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.ABOUT_US_MESSAGE)


# MARK: Teacher referrals

@dp.message_handler(lambda message: local.check_text([Data.TEACHER_REFERRAL_BUTTON], message.text)[0] and
                                    user_s.is_teacher(telegram_id=message.from_user.id))
async def teacher_referrals(message: types.Message):
    telegram_id = message.from_user.id
    referral = user_s.get_teacher_referral(telegram_id)
    await send_message_and_buttons(message, buttons=[Data.MAIN_MENU_BUTTON], state=Data.TEACHER_REFERRAL_MESSAGE)
    await message.answer(referral)


# MARK: Subject set state

@dp.message_handler(state=SubjectsStates.all_states)
async def subject_set_state(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id)
    current_state = await state.get_state()
    if current_state == SubjectsStates.SUBJECTS_STATE_0.state:
        await state.set_state(SubjectsStates.SUBJECTS_STATE_1)
        subject = local.check_text(local.subjects, message.text)[1]
        await user_s.set_student_subjects(telegram_id, 1, subject)
        await send_message_and_buttons(message, buttons=local.subjects + [Data.CANCEL_BUTTON],
                                       state=Data.CHOOSE_TOPIC_MESSAGE)
    else:
        await state.finish()
        subject = local.check_text(local.subjects, message.text)[1]
        await user_s.set_student_subjects(telegram_id, 2, subject)
        profile_info = user_s.get_user_profile(telegram_id=telegram_id, user_language=language)
        await send_message_and_buttons(message, buttons=local.profile, state=Data.PROFILE_MESSAGE,
                                       args=[profile_info])


# MARK: Subject profile

@dp.message_handler(lambda message: local.check_text([Data.SUBJECT_BUTTON], message.text)[0])
async def subject_profile(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await state.set_state(SubjectsStates.SUBJECTS_STATE_0)
    await send_message_and_buttons(message, buttons=local.subjects + [Data.CANCEL_BUTTON],
                                   state=Data.CHOOSE_TOPIC_MESSAGE)


# MARK: Profile

@dp.message_handler(lambda message: local.check_text([Data.PROFILE_BUTTON], text=message.text)[0] or
                                    message.text == "/profile")
async def profile(message: types.Message):
    telegram_id = message.from_user.id
    language = user_s.get_language(telegram_id)
    profile_info = user_s.get_user_profile(telegram_id=telegram_id, user_language=language)
    await send_message_and_buttons(message, buttons=local.profile, state=Data.PROFILE_MESSAGE,
                                   args=[profile_info])



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
