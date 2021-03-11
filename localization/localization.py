class Localization:
    languages = ["Қазақ", "Русский"]
    subjects = ["Қазақстан Тарихы", "Қазақ тілі", "История Казахстана", "География рус", "Биология рус"]
    data = {
        "languages": {
            "Русский": "Русский",
            "Қазақ": "Қазақ"
        },
        "start button": {
            "Русский": "Начать тест",
            "Қазақ": "Тест бастау"
        },
        "start message": {
            "Русский": "Здравствуйте чтобы начать нажмите кнопку",
            "Қазақ": "Саламатсызба бастау үшін батырманы басыныз"
        },
        "select message": {
            "Русский": "Выберете предмет",
            "Қазақ": "Пән таңданыз"
        },
        "restart message": {
            "Русский": "Чтобы начать новый тест, нажмите на кнопку.",
            "Қазақ": "Қайтып бастау үшін батырманы басыныз"
        },
        "result message": {
            "Русский": "Вы ответили правильно на {0} из {1}",
            "Қазақ": "{1} ішінде {0} дурыс"
        },
        "quiz number message": {
            "Русский": "Количество вопросов {}",
            "Қазақ": "Сұрақ саны {}"
        },
        "Қазақстан Тарихы": {
            "Русский": "История Казахстана (каз. яз.)",
            "Қазақ": "Қазақстан тарихы (қаз. т.)"
        },
        "Қазақ тілі": {
            "Русский": "Казахский язык",
            "Қазақ": "Қазақ тілі"
        },
        "История Казахстана": {
            "Русский": "История Казахстана (рус. яз.)",
            "Қазақ": "Қазақстан тарихы (о. т.)"
        },
        "География рус": {
            "Русский": "География (рус. яз.)",
            "Қазақ": "География (о. т.)"
        },
        "Биология рус": {
            "Русский": "Биология (рус. яз.)",
            "Қазақ": "Биология (о. т.)"
        }
    }

    def get_key(self, text):
        for key, data in self.data.items():
            for language, data_language in data.items():
                if data_language == text:
                    return key

    def get_text(self, text, telegram_id, user_s):
        try:
            return self.data[text][user_s.get_user_language(telegram_id=telegram_id)]
        except Exception as e:
            print(e)

    def check_text(self, texts, message):
        for text in texts:
            for language, language_text in self.data[text].items():
                if language_text == message:
                    return True
        return False
