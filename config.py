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
    USER_STATE = ["Teacher", "Student", "Tutor"]
    SUBJECT_NAMES = ["Қазақ тілі", "Русский язык all", "География ru", "География kz", "Ағылшын тілі ru",
                     "Ағылшын тілі kz", "Қазақстан тарихы kz", "Қазақстан тарихы ru", "Биология ru",
                     "Биология kz", "Дүние жүзі тарихы ru", "Дүние жүзі тарихы kz", "Әдебиет ru", "Әдебиет kz",
                     "Математика rus", "Физика rus"]
    DATA_SUBJECT_NAME = {
        Data.PHYS_RUS: "Физика rus",
        Data.MATH_RUS: "Математика rus",
        Data.KAZAKH_LANGUAGE: "Қазақ тілі",
        Data.RUSSIAN_LANGUAGE: "Русский язык all",
        Data.BIOLOGY_RUS: "Биология ru",
        Data.BIOLOGY_KAZ: "Биология kz",
        Data.KAZ_HISTORY_KAZ: "Қазақстан тарихы kz",
        Data.KAZ_HISTORY_RUS: "Қазақстан тарихы ru",
        Data.GEOGRAPHY_RUS: "География ru",
        Data.GEOGRAPHY_KAZ: "География kz",
        Data.ENGLISH_KAZ: "Ағылшын тілі kz",
        Data.ENGLISH_RUS: "Ағылшын тілі ru",
        Data.WORLD_HISTORY_RUS: "Дүние жүзі тарихы ru",
        Data.WORLD_HISTORY_KAZ: "Дүние жүзі тарихы kz",
        Data.LITERATURE_KAZ: "Әдебиет kz",
        Data.LITERATURE_RUS: "Әдебиет ru"
    }
    SUBJECT_NAME_DATA = {
        "Физика rus": Data.PHYS_RUS,
        "Математика rus": Data.MATH_RUS,
        "Қазақ тілі": Data.KAZAKH_LANGUAGE,
        "Русский язык all": Data.RUSSIAN_LANGUAGE,
        "География ru": Data.GEOGRAPHY_RUS,
        "География kz": Data.GEOGRAPHY_KAZ,
        "Ағылшын тілі ru": Data.ENGLISH_RUS,
        "Ағылшын тілі kz": Data.ENGLISH_KAZ,
        "Биология ru": Data.BIOLOGY_RUS,
        "Биология kz": Data.BIOLOGY_KAZ,
        "Қазақстан тарихы kz": Data.KAZ_HISTORY_KAZ,
        "Қазақстан тарихы ru": Data.KAZ_HISTORY_RUS,
        "Дүние жүзі тарихы kz": Data.WORLD_HISTORY_KAZ,
        "Дүние жүзі тарихы ru": Data.WORLD_HISTORY_RUS,
        "Әдебиет kz": Data.LITERATURE_KAZ,
        "Әдебиет ru": Data.LITERATURE_RUS
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
