import os
from data.models import User, Student, Teacher, Tutor
from localization.localization import Data


class Config:
    API_URL = 'http://aldie1741.pythonanywhere.com/'
    TOKEN = os.getenv('API_BOT_TOKEN')
    HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
    WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
    WEBHOOK_PATH = f'/webhook/{TOKEN}'
    WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
    WEBAPP_HOST = '0.0.0.0'
    WEBAPP_PORT = int(os.getenv('PORT'))
    USERS = "users"
    TEACHERS = "teachers"
    STUDENTS = "students"
    TUTORS = "tutors"
    USER_DB = [USERS, TEACHERS, STUDENTS]
    SUBJECTS_DB = "subjects"
    SUBTOPIC_DB = "subtopic"
    QUIZ_SET_DB = "quizset"
    USER_STATE = ["Teacher", "Student", "Tutor"]
    SUBJECT_NAMES = ["Химия ru", "Биология ru", "География ru", "Всемирная история ru", "Право ru",
                     "Русский язык", "Русская литература", "Английский язык", "Математика ru",
                     "Физика ru", "Грамотность чтения ru", "История Казахстана ru", "Математическая грамотность ru"]
    DATA_SUBJECT_NAME = {
        Data.ENT: "Ент",
        Data.RIGHT_RUS: "Право ru",
        Data.CHEMISTRY_RUS: "Химия ru",
        Data.BIOLOGY_RUS: "Биология ru",
        Data.GEOGRAPHY_RUS: "География ru",
        Data.WORLD_HISTORY_RUS: "Всемирная история ru",
        Data.RUSSIAN_LANGUAGE: "Русский язык",
        Data.LITERATURE_RUS: "Русская литература",
        Data.ENGLISH_LANGUAGE: "Английский язык",
        Data.MATH_RUS: "Математика ru",
        Data.PHYS_RUS: "Физика ru",
        Data.READING_LITERACY_RUS: "Грамотность чтения ru",
        Data.KAZ_HISTORY_RUS: "История Казахстана ru",
        Data.MATH_LITERACY_RUS: "Математическая грамотность ru"
    }
    SUBJECT_NAME_DATA = {
        "Право ru": Data.RIGHT_RUS,
        "Химия ru": Data.CHEMISTRY_RUS,
        "Биология ru": Data.BIOLOGY_RUS,
        "География ru": Data.GEOGRAPHY_RUS,
        "Всемирная история ru": Data.WORLD_HISTORY_RUS,
        "Русский язык": Data.RUSSIAN_LANGUAGE,
        "Русская литература": Data.LITERATURE_RUS,
        "Английский язык": Data.ENGLISH_LANGUAGE,
        "Математика ru": Data.MATH_RUS,
        "Физика ru": Data.PHYS_RUS,
        "Грамотность чтения ru": Data.READING_LITERACY_RUS,
        "История Казахстана ru": Data.KAZ_HISTORY_RUS,
        "Математическая грамотность ru": Data.MATH_LITERACY_RUS,
    }
    QUIZ_DB = "questions"
    SESSION_DB = "sessions"
    USER_TYPE_FIELDS = {
        USERS: ["current_type", "telegram_id", "selected_language"],
        TEACHERS: ["telegram_id", "selected_language", "referral", "students"],
        STUDENTS: ["telegram_id", "selected_language"]
    }
    DATA_USER_STATE = {
        Data.TEACHER: "Teacher",
        Data.STUDENT: "Student",
        Data.TUTOR: "Tutor"
    }
    USER_STATE_DATA = {
        "Teacher": Data.TEACHER,
        "Student": Data.STUDENT,
        "Tutor": Data.TUTOR
    }
    LANGUAGE_DATA = {
        "Русский": Data.RUSSIAN,
        "Қазақ": Data.KAZAKH
    }
    DATA_LANGUAGE = {
        Data.RUSSIAN: "Русский",
        Data.KAZAKH: "Қазақ"
    }
    # students, referral, telegram_id, selected_language
    USER_TYPE_MODEL = {
        USERS: User,
        STUDENTS: Student,
        TEACHERS: Teacher,
        TUTORS: Tutor
    }
    # ADMIN_IDS = [int(i) for i in os.getenv('OWNER_ID').split()]
