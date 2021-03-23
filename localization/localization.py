from enum import Enum, auto


class Data(Enum):
    NEW_USERS_WELCOME_MESSAGE = 0
    WELCOME_MESSAGE = 1
    KAZAKH = 2
    MAIN_MENU_BUTTON = 3
    NOT_REGISTERED_MESSAGE = 4
    SET_LANGUAGE_MESSAGE = 5
    MAIN_MENU_MESSAGE = 6
    USER_NAME_BUTTON = 7
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
    CHOOSE_TOPIC_MESSAGE = 28
    CANCEL_BUTTON = 29
    START_SESSION_MESSAGE = 30
    RESULTS_MESSAGE = 31
    INPUT_REFERRAL_MESSAGE = 32
    TEACHER_ADD_SUCCESS_MESSAGE = 33
    TEACHER_ADD_UN_SUCCESS_MESSAGE = 34
    STUDENT_PAYMENT_MESSAGE = 35
    TEACHER_STATS_BUTTON = 37
    TEACHER_PAYMENT_MESSAGE = 38
    TEACHER_REFERRAL_BUTTON = 39
    TEACHER_REFERRAL_MESSAGE = 40
    STUDENT_STATS_MESSAGE = 41
    PROFILE_MESSAGE = 42
    LANGUAGE_BUTTON = 43
    USER_STATE_BUTTON = 44
    PROFILE_BUTTON = 45
    RUSSIAN = 46
    SET_NAME_SUCCESS_MESSAGE = 47
    INPUT_NAME_MESSAGE = 48
    SUBJECT_INFO_FORMAT_MESSAGE = 49
    SUBJECT_INFO_MESSAGE = 50
    DELETE_STUDENT_FROM_TEACHER_BUTTON = 51
    DELETE_STUDENT_FROM_TEACHER_MESSAGE = 52
    ENGLISH_RUS = 53
    ENGLISH_KAZ = 54
    WORLD_HISTORY_RUS = 55
    WORLD_HISTORY_KAZ = 56
    LITERATURE_RUS = 57
    LITERATURE_KAZ = 58
    ANSWER_BELOW = 59
    TEACHER_DELETE_STUDENT_SUCCESS_MESSAGE = 60
    TEACHER_DELETE_STUDENT_UN_SUCCESS_MESSAGE = 61
    MATH_RUS = 62
    PHYS_RUS = 63
    CHOOSE_SUBTOPIC_MESSAGE = 64


class Localization:
    options = ["A)", "B)", "C)", "D)", "E)", "F)", "G)", "H)"]
    languages = [Data.KAZAKH, Data.RUSSIAN]
    student_main_menu_buttons = [Data.START_QUIZ_BUTTON, Data.ADD_TEACHER_BUTTON, Data.STUDENT_STATS_BUTTON,
                                 Data.SYNOPSES_BUTTON, Data.PAYMENT_BUTTON, Data.PROFILE_BUTTON]
    teacher_main_menu_buttons = [Data.PAYMENT_BUTTON, Data.TEACHER_STATS_BUTTON, Data.TEACHER_REFERRAL_BUTTON,
                                 Data.PROFILE_BUTTON]
    user_state_buttons = [Data.TEACHER, Data.STUDENT]
    subjects = [Data.KAZ_HISTORY_KAZ, Data.KAZ_HISTORY_RUS, Data.KAZAKH_LANGUAGE, Data.RUSSIAN_LANGUAGE,
                Data.GEOGRAPHY_KAZ, Data.GEOGRAPHY_RUS, Data.BIOLOGY_KAZ, Data.BIOLOGY_RUS, Data.ENGLISH_KAZ,
                Data.ENGLISH_RUS, Data.WORLD_HISTORY_KAZ, Data.WORLD_HISTORY_RUS, Data.LITERATURE_KAZ,
                Data.LITERATURE_RUS, Data.MATH_RUS, Data.PHYS_RUS]
    image_subjects = [Data.MATH_RUS, Data.PHYS_RUS]
    profile = [Data.LANGUAGE_BUTTON, Data.USER_STATE_BUTTON, Data.USER_NAME_BUTTON, Data.MAIN_MENU_BUTTON]
    synopses_subjects = [Data.KAZ_HISTORY_KAZ, Data.MAIN_MENU_BUTTON]
    data = {
        Data.CHOOSE_SUBTOPIC_MESSAGE: {
            Data.RUSSIAN: "Выберите тему",
            Data.KAZAKH: "Теманы таңданыз"
        },
        Data.PHYS_RUS: {
            Data.RUSSIAN: "Физика (рус. яз.) (demo)",
            Data.KAZAKH: "Физика (о. т.) (demo)"
        },
        Data.MATH_RUS: {
            Data.RUSSIAN: "Математика (рус. яз.) (demo)",
            Data.KAZAKH: "Математика (о. т.) (demo)"
        },
        Data.TEACHER_DELETE_STUDENT_UN_SUCCESS_MESSAGE: {
            Data.RUSSIAN: "Вы ввели не верные данные попробуйте снова",
            Data.KAZAKH: "Сіз қате деректерді енгіздіңіз қайталап көріңіз"
        },
        Data.TEACHER_DELETE_STUDENT_SUCCESS_MESSAGE: {
            Data.RUSSIAN: "Ученик успешно удален",
            Data.KAZAKH: "Оқушы сәтті өшірілді"
        },
        Data.ANSWER_BELOW: {
            Data.RUSSIAN: "Ответте на вопрос выше",
            Data.KAZAKH: "Үстіндегі сұраққа жауап берініз"
        },
        Data.LITERATURE_KAZ: {
            Data.RUSSIAN: "Казахская литература",
            Data.KAZAKH: "Қазақ әдебиеті"
        },
        Data.LITERATURE_RUS: {
            Data.RUSSIAN: "Русская литература",
            Data.KAZAKH: "Орыс әдебиеті"
        },
        Data.WORLD_HISTORY_KAZ: {
            Data.RUSSIAN: "Всемирная история (каз. яз.)",
            Data.KAZAKH: "Всемирная история (қаз. т.)"
        },
        Data.WORLD_HISTORY_RUS: {
            Data.RUSSIAN: "Всемирная история (рус. яз.)",
            Data.KAZAKH: "Всемирная история (о. т.)"
        },
        Data.ENGLISH_KAZ: {
            Data.RUSSIAN: "Английский язык (каз. яз.)",
            Data.KAZAKH: "Ағылшын тілі (қаз. т.)"
        },
        Data.ENGLISH_RUS: {
            Data.RUSSIAN: "Английский язык (рус. яз.)",
            Data.KAZAKH: "Ағылшын тілі (о. т.)"
        },
        Data.DELETE_STUDENT_FROM_TEACHER_MESSAGE: {
            Data.RUSSIAN: "Выберите какого ученика вы хотите удалить",
            Data.KAZAKH: "Өшіргініз келіп тұрган оқушыны танданыз"
        },
        Data.DELETE_STUDENT_FROM_TEACHER_BUTTON: {
            Data.RUSSIAN: "Удалить ученика",
            Data.KAZAKH: "Оқушыны өшіру"
        },
        Data.SUBJECT_INFO_FORMAT_MESSAGE: {
            Data.RUSSIAN: "Предмет / Количество вопросов / Доля правильных",
            Data.KAZAKH: "Пән / Сурақ саны / Дурыс бөлшегі"
        },
        Data.INPUT_NAME_MESSAGE: {
            Data.RUSSIAN: "Введите имя",
            Data.KAZAKH: "Есімінізді енгізініз"
        },
        Data.SET_NAME_SUCCESS_MESSAGE: {
            Data.RUSSIAN: "Имя успешно изменено",
            Data.KAZAKH: "Есімініз сәтті өзгертілді"
        },
        Data.RUSSIAN: {
            Data.RUSSIAN: "Русский",
            Data.KAZAKH: "Орысша"
        },
        Data.KAZAKH: {
            Data.RUSSIAN: "Казахский",
            Data.KAZAKH: "Қазақша"
        },
        Data.PROFILE_BUTTON: {
            Data.RUSSIAN: "Профиль",
            Data.KAZAKH: "Профиль"
        },
        Data.PROFILE_MESSAGE: {
            Data.RUSSIAN: "Ваш профиль:\n{}",
            Data.KAZAKH: "Сіздін профилініз:\n{}"
        },
        Data.USER_STATE_BUTTON: {
            Data.RUSSIAN: "Режим",
            Data.KAZAKH: "Режим"
        },
        Data.LANGUAGE_BUTTON: {
            Data.RUSSIAN: "Язык",
            Data.KAZAKH: "Тіл"
        },
        Data.USER_NAME_BUTTON: {
            Data.RUSSIAN: "Имя",
            Data.KAZAKH: "Есім"
        },
        Data.STUDENT_STATS_MESSAGE: {
            Data.RUSSIAN: "Имя: {}\nКоличество правильных ответов за все время: {}\n"
                          "Общее количество ответов за все время: {}\nКоличество правильных ответов за 7 дней: {}\n"
                          "Общее количество ответов за 7 дней: {}\nДата создания: {}\n",
            Data.KAZAKH: "Есімі: {}\nДурыс жауап саны: {}\n"
                         "Жауап жалпы саны : {}\n7 күнгі дурыс жауап саны: {}\n"
                         "7 күнгі жалпы жауап саны: {}\nТіркелу күні: {}\n",
        },
        Data.TEACHER_REFERRAL_MESSAGE: {
            Data.RUSSIAN: "Ваша реферальная ссылка",
            Data.KAZAKH: "Сіздің реферал сілтеменіз"
        },
        Data.TEACHER_REFERRAL_BUTTON: {
            Data.RUSSIAN: "Реферальная ссылка",
            Data.KAZAKH: "Реферал сілтеме"
        },
        Data.TEACHER_PAYMENT_MESSAGE: {
            Data.RUSSIAN: "Поддержать разработчиков:\n+77082953401\n+77088948540\n",
            Data.KAZAKH: "Әзірлеушілерді қолдау:\n+77082953401\n+77088948540\n"
        },
        Data.TEACHER_STATS_BUTTON: {
            Data.RUSSIAN: "Статистика учеников",
            Data.KAZAKH: "Оқушылар статистикасы"
        },
        Data.STUDENT_PAYMENT_MESSAGE: {
            Data.RUSSIAN: "Поддержать разработчиков:\n+77082953401\n+77088948540\n",
            Data.KAZAKH: "Әзірлеушілерді қолдау:\n+77082953401\n+77088948540\n"
        },
        Data.TEACHER_ADD_UN_SUCCESS_MESSAGE: {
            Data.RUSSIAN: "Учителя с таким кодом не существует\nПопробуйте заново",
            Data.KAZAKH: "Мұндай кодпен ұстаз жоқ\nҚайтадан көрініз"
        },
        Data.TEACHER_ADD_SUCCESS_MESSAGE: {
            Data.RUSSIAN: "Вы были успешно добавлены к учителю",
            Data.KAZAKH: "Сіз ұстаға сәтті тіркелдініз"
        },
        Data.INPUT_REFERRAL_MESSAGE: {
            Data.RUSSIAN: "Введите код",
            Data.KAZAKH: "Кодты енгізініз"
        },
        Data.RESULTS_MESSAGE: {
            Data.RUSSIAN: "Ваш результат: {} : {}",
            Data.KAZAKH: "Cіздің нәтиженіз: {} : {}"
        },
        Data.CANCEL_BUTTON: {
            Data.RUSSIAN: "Отмена",
            Data.KAZAKH: "Бас тарту"
        },
        Data.START_SESSION_MESSAGE: {
            Data.RUSSIAN: "Предмет: {}, Общее количество вопросов: {}",
            Data.KAZAKH: "Сабақ: {}, Сұрақ жалпы саны: {}"
        },
        Data.CHOOSE_TOPIC_MESSAGE: {
            Data.RUSSIAN: "Выберите предмет",
            Data.KAZAKH: "Сабақты таңданыз"
        },
        Data.KAZ_HISTORY_RUS: {
            Data.RUSSIAN: "История Казахстана (рус.яз.)",
            Data.KAZAKH: "Қазақстан Тарихы (о. т.)"
        },
        Data.KAZ_HISTORY_KAZ: {
            Data.RUSSIAN: "История Казахстана (каз. яз.)",
            Data.KAZAKH: "Қазақстан Тарихы (қаз. т.)"
        },
        Data.BIOLOGY_KAZ: {
            Data.RUSSIAN: "Биология (каз. яз.)",
            Data.KAZAKH: "Биология (қаз. т.)"
        },
        Data.BIOLOGY_RUS: {
            Data.RUSSIAN: "Биология (рус.яз.)",
            Data.KAZAKH: "Биология (о. т.)"
        },
        Data.GEOGRAPHY_RUS: {
            Data.RUSSIAN: "География (рус.яз.)",
            Data.KAZAKH: "География (о. т.)"
        },
        Data.GEOGRAPHY_KAZ: {
            Data.RUSSIAN: "География (каз. яз.)",
            Data.KAZAKH: "География (қаз. т.)"
        },
        Data.RUSSIAN_LANGUAGE: {
            Data.RUSSIAN: "Русский язык",
            Data.KAZAKH: "Орыс тілі"
        },
        Data.KAZAKH_LANGUAGE: {
            Data.RUSSIAN: "Казахский язык",
            Data.KAZAKH: "Қазақ тілі"
        },
        Data.IN_MAIN_MENU_MESSAGE: {
            Data.RUSSIAN: "Выберите сервис",
            Data.KAZAKH: "Сервис танданыз"
        },
        Data.PAYMENT_BUTTON: {
            Data.RUSSIAN: "Платежи",
            Data.KAZAKH: "Толемдер"
        },
        Data.SYNOPSES_BUTTON: {
            Data.RUSSIAN: "Конспекты",
            Data.KAZAKH: "Конспектер"
        },
        Data.STUDENT_STATS_BUTTON: {
            Data.RUSSIAN: "Статистика",
            Data.KAZAKH: "Статистика"
        },
        Data.ADD_TEACHER_BUTTON: {
            Data.RUSSIAN: "Добавиться к учителю",
            Data.KAZAKH: "Ұстазға қосылу"
        },
        Data.START_QUIZ_BUTTON: {
            Data.RUSSIAN: "Начать тест",
            Data.KAZAKH: "Тест бастау"
        },
        Data.SET_USER_STATE_MESSAGE: {
            Data.RUSSIAN: "Выберите режим",
            Data.KAZAKH: "Режимінізді таңданыз"
        },
        Data.TUTOR: {
            Data.RUSSIAN: "Репититор",
            Data.KAZAKH: "Репититор"
        },
        Data.STUDENT: {
            Data.RUSSIAN: "Ученик",
            Data.KAZAKH: "Оқушы"
        },
        Data.TEACHER: {
            Data.RUSSIAN: "Учитель",
            Data.KAZAKH: "Ұстаз"
        },
        Data.NEW_USERS_WELCOME_MESSAGE: {
            Data.RUSSIAN: "Здравствуйте, для настройки профиля и выбора языка используйте команду /profile",
            Data.KAZAKH: "Саламатсызба, профиль орнату немесе тіл тандау үшін /profile командасын қолданыныз\n"
        },
        Data.WELCOME_MESSAGE: {
            Data.RUSSIAN: "Здравствуйте, пройдите в главное меню",
            Data.KAZAKH: "Саламатсызба, басты менюге өтініз"
        },
        Data.MAIN_MENU_BUTTON: {
            Data.RUSSIAN: "Главное меню",
            Data.KAZAKH: "Басты меню"
        },
        Data.MAIN_MENU_MESSAGE: {
            Data.RUSSIAN: "Чтобы пройти в главное меню нажмите кнопку",
            Data.KAZAKH: "Басты менюге өту үшін батырманы басыныз"
        },
        Data.NOT_REGISTERED_MESSAGE: {
            Data.RUSSIAN: "Чтобы запустить бота используйте команду /start",
            Data.KAZAKH: "Ботты косу ушін /start командасын қолданыныз"
        },
        Data.SET_LANGUAGE_MESSAGE: {
            Data.RUSSIAN: "Выберите язык",
            Data.KAZAKH: "Тіл таңданыз"
        }
    }

    def check_text(self, states, text):
        for state in states:
            for language, language_text in self.data[state].items():
                if language_text == text:
                    return [True, state]
        return [False]
