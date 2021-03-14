from typing import List
from json import JSONEncoder


class Session:
    def __init__(self, telegram_id, topic_name, quiz_ids, results):
        self.telegram_id = telegram_id
        self.topic_name = topic_name
        self.quiz_ids = quiz_ids
        self.results = results


class Quiz:
    type: str = "question"

    def __init__(self, topic, quiz_id, question, options, correct_option_id, owner_id):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.topic: str = topic
        self.quiz_id: str = quiz_id  # ID викторины. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: List[str] = [*options]  # "Распакованное" содержимое массива m_options в массив options
        self.correct_option_id: int = correct_option_id  # ID правильного ответа
        self.owner: int = 0  # Владелец опроса
        self.message_id: int = 0  # Сообщение с викториной (для закрытия)

    def to_json(self):
        return {
            "topic": self.topic,

        }


class AbstractUser:
    def __init__(self, telegram_id):
        self.telegram_id: int = telegram_id  # ID юзера телеграм


class User(AbstractUser):

    def __init__(self, telegram_id, user_state="Student", selected_language="Русский"):
        super().__init__(telegram_id)
        self.selected_language = selected_language
        self.user_state = user_state

    def to_json(self):
        return {
            "telegram_id": self.telegram_id,
            "selected_language": self.selected_language,
            "user_state": self.user_state
        }


class Student(AbstractUser):
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


