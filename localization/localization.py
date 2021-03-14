from enum import Enum, auto


class Data(Enum):
    NEW_USERS_WELCOME_MESSAGE = 0
    WELCOME_MESSAGE = 1
    SET_LANGUAGE_BUTTON = 2
    MAIN_MENU_BUTTON = 3
    NOT_REGISTERED_MESSAGE = 4
    SET_LANGUAGE_MESSAGE = 5
    MAIN_MENU_MESSAGE = 6
    USER_STATE_BUTTONS = 7
    TEACHER = 8
    STUDENT = 9
    TUTOR = 10
    SET_USER_STATE_MESSAGE = 11
    SET_USER_STATE_RESULT_MESSAGE = 12
    START_QUIZ_BUTTON = 13
    IN_WORK_MESSAGE = 14
    ADD_TEACHER_BUTTON = 15
    STUDENT_STATS_BUTTON = 16
    SYNOPSES_BUTTON = 17  # Конспекты
    STUDENT_PAYMENT_BUTTON = 18
    STUDENT_MAIN_MENU_MESSAGE = 19
    RUSSIAN_LANGUAGE = 20
    KAZAKH_LANGUAGE = 21
    KAZ_HISTORY_KAZ = 22
    KAZ_HISTORY_RUS = 23
    GEOGRAPHY_RUS = 24
    GEOGRAPHY_KAZ = 25
    BIOLOGY_RUS = 26
    BIOLOGY_KAZ = 27
    CHOOSE_QUIZ_TOPIC_MESSAGE = 28
    CANCEL_SESSION_BUTTON = 29
    START_SESSION_MESSAGE = 30
    RESULTS_MESSAGE = 31


class Localization:
    languages = ["Қазақ", "Русский"]
    student_main_menu_buttons = [Data.START_QUIZ_BUTTON, Data.ADD_TEACHER_BUTTON, Data.STUDENT_STATS_BUTTON,
                                 Data.SYNOPSES_BUTTON, Data.STUDENT_PAYMENT_BUTTON]
    user_state_buttons = [Data.TEACHER, Data.STUDENT, Data.TUTOR]
    subjects = [Data.KAZ_HISTORY_KAZ, Data.KAZ_HISTORY_RUS, Data.KAZAKH_LANGUAGE, Data.RUSSIAN_LANGUAGE,
                Data.GEOGRAPHY_KAZ, Data.GEOGRAPHY_RUS, Data.BIOLOGY_RUS, Data.BIOLOGY_KAZ]
    data = {
        Data.RESULTS_MESSAGE: {
            "Русский": "Ваш результат: {} : {}",
            "Қазақ": "Cіздін нәтиженіз: {} : {}"
        },
        Data.CANCEL_SESSION_BUTTON: {
            "Русский": "Отмена",
            "Қазақ": "Бас тарту"
        },
        Data.START_SESSION_MESSAGE: {
            "Русский": "Предмет: {}, Общее количество вопросов: {}",
            "Қазақ": "Сабақ: {}, Сұрақ жалпы саны: {}"
        },
        Data.CHOOSE_QUIZ_TOPIC_MESSAGE: {
            "Русский": "Выберите предмет",
            "Қазақ": "Сабақты таңданыз"
        },
        Data.KAZ_HISTORY_RUS: {
            "Русский": "История Казахстана (рус.яз.)",
            "Қазақ": "Қазақстан Тарихы (о. т.)"
        },
        Data.KAZ_HISTORY_KAZ: {
            "Русский": "История Казахстана (каз. яз.)",
            "Қазақ": "Қазақстан Тарихы (қаз. т.)"
        },
        Data.BIOLOGY_KAZ: {
            "Русский": "Биология (каз. яз.)",
            "Қазақ": "Биология (қаз. т.)"
        },
        Data.BIOLOGY_RUS: {
            "Русский": "Биология (рус.яз.)",
            "Қазақ": "Биология (о. т.)"
        },
        Data.GEOGRAPHY_RUS: {
            "Русский": "География (рус.яз.)",
            "Қазақ": "География (о. т.)"
        },
        Data.GEOGRAPHY_KAZ: {
            "Русский": "География (каз. яз.)",
            "Қазақ": "География (қаз. т.)"
        },
        Data.RUSSIAN_LANGUAGE: {
            "Русский": "Руссский язык",
            "Қазақ": "Орыс тілі"
        },
        Data.KAZAKH_LANGUAGE: {
            "Русский": "Казахский язык",
            "Қазақ": "Қазақ тілі"
        },
        Data.STUDENT_MAIN_MENU_MESSAGE: {
            "Русский": "Выберите сервис",
            "Қазақ": "Сервис танданыз"
        },
        Data.STUDENT_PAYMENT_BUTTON: {
            "Русский": "Платежи",
            "Қазақ": "Толемдер"
        },
        Data.SYNOPSES_BUTTON: {
            "Русский": "Конспекты",
            "Қазақ": "Конспектер"
        },
        Data.STUDENT_STATS_BUTTON: {
            "Русский": "Статистика",
            "Қазақ": "Статистика"
        },
        Data.ADD_TEACHER_BUTTON: {
            "Русский": "Добавиться к учителю",
            "Қазақ": "Ұстазға қосылу"
        },
        Data.START_QUIZ_BUTTON: {
            "Русский": "Начать тест",
            "Қазақ": "Тест бастау"
        },
        Data.SET_USER_STATE_MESSAGE: {
            "Русский": "Выберите режим",
            "Қазақ": "Режимінізді таңданыз"
        },
        Data.TUTOR: {
            "Русский": "Репитито",
            "Қазақ": "Репититор"
        },
        Data.STUDENT: {
            "Русский": "Ученик",
            "Қазақ": "Оқушы"
        },
        Data.TEACHER: {
            "Русский": "Учитель",
            "Қазақ": "Ұстаз"
        },
        Data.USER_STATE_BUTTONS: {
            "Русский": ["Учитель", "Ученик", "Репититор"],
            "Қазақ": ["Ұстаз", "Оқушы", "Репититор"]
        },
        Data.NEW_USERS_WELCOME_MESSAGE: {
            "Русский": "Здравствуйте\nДля смены режима(Учитель, Ученик, Репититор) используйте команду /user_state\n"
                       "Для выбора языка используйте команду /language\n",
            "Қазақ": "Саламатсызба\nРежимінізді(Ұстаз, Оқушы, Репититор) өзгерту ушін /user_state "
                     "командасын колданыныз\nТіл таңдау үшін /language командасын колданыныз\n"
        },
        Data.WELCOME_MESSAGE: {
            "Русский": "Здравствуйте, пройдите в главное меню",
            "Қазақ": "Саламатсызба, басты менюге ютініз"
        },
        Data.SET_LANGUAGE_BUTTON: {
            "Русский": "Русский",
            "Қазақ": "Қазақ"
        },
        Data.MAIN_MENU_BUTTON: {
            "Русский": "Главное меню",
            "Қазақ": "Басты меню"
        },
        Data.MAIN_MENU_MESSAGE: {
            "Русский": "Чтобы пройти в главное меню нажмите кнопку",
            "Қазақ": "Басты менюге юту үшін батырманы басыныз"
        },
        Data.NOT_REGISTERED_MESSAGE: {
            "Русский": "Чтобы запустить бота используйте команду /start",
            "Қазақ": "Ботты косу ушін /start командасын қолданыныз"
        },
        Data.SET_LANGUAGE_MESSAGE: {
            "Русский": "Выберите язык",
            "Қазақ": "Тіл таңданыз"
        }
    }

    def check_text(self, states, text):
        for state in states:
            for language, language_text in self.data[state].items():
                if language_text == text:
                    return [True, state]
        return [False]
