from typing import List
from json import JSONEncoder
from localization.localization import Data
import config


class Session:
    def __init__(self, telegram_id, topic_name, quiz_ids, results):
        self.telegram_id = telegram_id
        self.topic_name = topic_name
        self.quiz_ids = quiz_ids
        self.results = results


class Subtopic:
    def __init__(self, topic_id, topic_name, text):
        self.topic_id = topic_id,
        self.topic_name = topic_name,
        self.text = text


class Subject:
    def __init__(self, topic_name, subtopics):
        self.topic_name = topic_name,
        self.subtopics = subtopics


class QuizSet:
    def __init__(self, text, quizzes):
        self.quizzes = quizzes
        self.text = text


class Quiz:
    type: str = "question"

    def __init__(self, topic, quiz_id, question, options, correct_option_id, is_image):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.topic: str = topic
        self.quiz_id: str = quiz_id  # ID викторины. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: List[str] = [*options]  # "Распакованное" содержимое массива m_options в массив options
        self.correct_option_id: int = correct_option_id  # ID правильного ответа
        self.owner: int = 0  # Владелец опроса
        self.message_id: int = 0  # Сообщение с викториной (для закрытия)
        self.is_image: bool = is_image

    def to_json(self):
        return {
            "topic": self.topic
        }


class AbstractUser:
    def __init__(self, telegram_id):
        self.telegram_id: int = telegram_id  # ID юзера телеграм


class User(AbstractUser):

    def __init__(self, telegram_id, user_state=Data.STUDENT, selected_language=Data.RUSSIAN, name=""):
        super().__init__(telegram_id)
        if name == "":
            self.name = "User-" + str(telegram_id % 100)
        else:
            self.name = name
        self.selected_language = selected_language
        self.user_state = user_state

    def to_json(self):
        return {
            "telegram_id": self.telegram_id,
            "name": self.name,
            "selected_language": config.Config.DATA_LANGUAGE[self.selected_language],
            "user_state": config.Config.DATA_USER_STATE[self.user_state]
        }


class Student(AbstractUser):
    def __init__(self, telegram_id, subject_1=Data.MATH_RUS, subject_2=Data.GEOGRAPHY_RUS):
        super().__init__(telegram_id)
        self.subject_1 = subject_1
        self.subject_2 = subject_2
    
    def to_json(self):
        return {
            "telegram_id": self.telegram_id,
        }


class Teacher(AbstractUser):
    def __init__(self, telegram_id, students=None, referral=None):
        super().__init__(telegram_id)
        if students is None:
            students = []
        if referral is None:
            referral = ""
        self.students = students
        self.referral = referral

    def to_json(self):
        return {
            "telegram_id": self.telegram_id,
            "students": self.students,
        }


class Tutor(AbstractUser):
    def to_json(self):
        return {
            "telegram_id": self.telegram_id,
        }


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


