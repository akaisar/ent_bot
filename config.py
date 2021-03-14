import os
from data.models import User, Student, Teacher, Tutor
from localization.localization import Data


class Config:
    API_URL = 'http://aldie1741.pythonanywhere.com/'
    TOKEN = os.getenv('API_BOT_TOKEN')
    USERS = "users"
    TEACHERS = "teachers"
    STUDENTS = "students"
    TUTORS = "tutors"
    USER_DB = [USERS, TEACHERS, STUDENTS]
    USER_STATE = ["Teacher", "Student", "Tutor"]
    DATA_USER_STATE = {
        Data.TEACHER: "Teacher",
        Data.STUDENT: "Student",
        Data.TUTOR: "Tutor"
    }
    DATA_SUBJECT_NAME = {
        Data.KAZAKH_LANGUAGE: "Қазақ тілі",
        Data.RUSSIAN_LANGUAGE: "Қазақ тілі",
        Data.BIOLOGY_RUS: "Қазақ тілі",
        Data.BIOLOGY_KAZ: "Қазақ тілі",
        Data.KAZ_HISTORY_KAZ: "Қазақ тілі",
        Data.KAZ_HISTORY_RUS: "Қазақ тілі",
        Data.GEOGRAPHY_RUS: "Қазақ тілі",
        Data.GEOGRAPHY_KAZ: "Қазақ тілі"
    }
    QUIZ_DB = "questions"
    SESSION_DB = "sessions"
    USER_TYPE_FIELDS = {
        USERS: ["current_type", "telegram_id", "selected_language"],
        TEACHERS: ["telegram_id", "selected_language", "referral", "students"],
        STUDENTS: ["telegram_id", "selected_language"]
    }
    # students, referral, telegram_id, selected_language
    USER_TYPE_MODEL = {
        USERS: User,
        STUDENTS: Student,
        TEACHERS: Teacher,
        TUTORS: Tutor
    }
    # ADMIN_IDS = [int(i) for i in os.getenv('OWNER_ID').split()]
