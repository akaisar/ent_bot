from typing import List
from json import JSONEncoder


class Quiz:
    type: str = "quiz"

    def __init__(self, quiz_id, question, options, correct_option_id, owner_id):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.quiz_id: str = quiz_id  # ID викторины. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: List[str] = [*options]  # "Распакованное" содержимое массива m_options в массив options
        self.correct_option_id: int = correct_option_id  # ID правильного ответа
        self.owner: int = owner_id  # Владелец опроса
        self.winners: List[int] = []  # Список победителей
        self.chat_id: int = 0  # Чат, в котором опубликована викторина
        self.message_id: int = 0  # Сообщение с викториной (для закрытия)


class User:
    def __init__(self, telegram_id):
        self.telegram_id: int = telegram_id  # ID юзера телеграм


class Question:
    type: str = "question"

    def __init__(self, topic, quiz_id, question, options, correct_option_id, owner_id):
        # Используем подсказки типов, чтобы было проще ориентироваться.
        self.topic: str = topic
        self.quiz_id: str = quiz_id  # ID викторины. Изменится после отправки от имени бота
        self.question: str = question  # Текст вопроса
        self.options: str = ' '.join(
            map(str, [*options]))  # "Распакованное" содержимое массива m_options в массив options
        self.correct_option_id: int = correct_option_id  # ID правильного ответа
        self.owner: int = owner_id  # Владелец опроса
        self.chat_id: int = 0  # Чат, в котором опубликована викторина
        self.message_id: int = 0  # Сообщение с викториной (для закрытия)


class Student(User):
    def __init__(self, completed_quizzes, telegram_id):
        super().__init__(telegram_id)
        self.completed_quizzes = completed_quizzes


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


