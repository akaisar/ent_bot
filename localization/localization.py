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
    PAYMENT_BUTTON = 18
    IN_MAIN_MENU_MESSAGE = 19
    RUSSIAN_LANGUAGE = 20
    KAZAKH_LANGUAGE = 21
    KAZ_HISTORY_KAZ = 22
    KAZ_HISTORY_RUS = 23
    GEOGRAPHY_RUS = 24
    GEOGRAPHY_KAZ = 25
    BIOLOGY_RUS = 26
    BIOLOGY_KAZ = 27
    CHOOSE_QUIZ_TOPIC_MESSAGE = 28
    CANCEL_BUTTON = 29
    START_SESSION_MESSAGE = 30
    RESULTS_MESSAGE = 31
    INPUT_REFERRAL_MESSAGE = 32
    TEACHER_ADD_SUCCESS_MESSAGE = 33
    TEACHER_ADD_UNSUCCESS_MESSAGE = 34
    STUDENT_PAYMENT_MESSAGE = 35
    TEACHER_STATS_BUTTON = 37
    TEACHER_PAYMENT_MESSAGE = 38
    TEACHER_REFERRAL_BUTTON = 39
    TEACHER_REFERRAL_MESSAGE = 40
    STUDENT_STATS_MESSAGE = 41


class Localization:
    languages = ["Қазақ", "Русский"]
    student_main_menu_buttons = [Data.START_QUIZ_BUTTON, Data.ADD_TEACHER_BUTTON, Data.STUDENT_STATS_BUTTON,
                                 Data.SYNOPSES_BUTTON, Data.PAYMENT_BUTTON]
    teacher_main_menu_buttons = [Data.PAYMENT_BUTTON, Data.TEACHER_STATS_BUTTON, Data.TEACHER_REFERRAL_BUTTON]
    user_state_buttons = [Data.TEACHER, Data.STUDENT, Data.TUTOR]
    subjects = [Data.KAZ_HISTORY_KAZ, Data.KAZ_HISTORY_RUS, Data.KAZAKH_LANGUAGE, Data.RUSSIAN_LANGUAGE,
                Data.GEOGRAPHY_KAZ, Data.GEOGRAPHY_RUS, Data.BIOLOGY_RUS, Data.BIOLOGY_KAZ]
    data = {
        Data.STUDENT_STATS_MESSAGE: {
            "Русский": "Telegram id: {}\nКоличество правильных ответов за все время: {}\n"
                       "Общее количество ответов за все время: {}\nКоличество правильных ответов за 7 дней: {}\n"
                       "Общее количество ответов за 7 дней: {}\nДата создания: {}",
            "Қазақ": "Telegram id: {}\nДурыс жауап саны: {}\n"
                     "Жауап жалпы саны : {}\n7 күнгі дурыс жауап саны: {}\n"
                     "7 күнгі жалпы жауап саны: {}\nТіркелу күні: {}",
        },
        Data.TEACHER_REFERRAL_MESSAGE: {
            "Русский": "Ваша реферальная ссылка {}",
            "Қазақ": "Сіздің реферал сілтеменіз {}"
        },
        Data.TEACHER_REFERRAL_BUTTON: {
            "Русский": "Реферальная ссылка",
            "Қазақ": "Реферал сілтеме"
        },
        Data.TEACHER_PAYMENT_MESSAGE: {
            "Русский": "Поддержать разработчиков:\n+77082953401\n+77088948540\n",
            "Қазақ": "Әзірлеушілерді қолдау:\n+7082953401\n+77088948540\n"
        },
        Data.TEACHER_STATS_BUTTON: {
            "Русский": "Статистика учеников",
            "Қазақ": "Оқушылар статистикасы"
        },
        Data.STUDENT_PAYMENT_MESSAGE: {
            "Русский": "Поддержать разработчиков:\n+77082953401\n+77088948540\n",
            "Қазақ": "Әзірлеушілерді қолдау:\n+7082953401\n+77088948540\n"
        },
        Data.TEACHER_ADD_UNSUCCESS_MESSAGE: {
            "Русский": "Учителя с таким кодом не существует\nПопробуйте заново",
            "Қазақ": "Мұндай кодпен ұстаз жоқ\nҚайтадан көрініз"
        },
        Data.TEACHER_ADD_SUCCESS_MESSAGE: {
            "Русский": "Вы были успешно добавлены к учителю\nЧтобы вернуться в меню нажмите кнопку",
            "Қазақ": "Сіз ұстаға сәтті тіркелдініз\nҚайту үшін батырманы басыныз"
        },
        Data.INPUT_REFERRAL_MESSAGE: {
            "Русский": "Введите код",
            "Қазақ": "Кодты енгізініз"
        },
        Data.RESULTS_MESSAGE: {
            "Русский": "Ваш результат: {} : {}",
            "Қазақ": "Cіздің нәтиженіз: {} : {}"
        },
        Data.CANCEL_BUTTON: {
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
        Data.IN_MAIN_MENU_MESSAGE: {
            "Русский": "Выберите сервис",
            "Қазақ": "Сервис танданыз"
        },
        Data.PAYMENT_BUTTON: {
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
            "Русский": "Репититор",
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
            "Қазақ": "Саламатсызба, басты менюге өтініз"
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
            "Қазақ": "Басты менюге өту үшін батырманы басыныз"
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
