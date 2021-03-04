class Localization:
    languages = ["Қазақ", "Русский"]
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
            "Қазақ": "Тіл таңданыз"
        },
        "restart message": {
            "Русский": "Чтобы начать новый тест, нажмите на кнопку.",
            "Қазақ": "Қайтып бастау үшін батырманы басыныз"
        },
        "result message": {
            "Русский": "Вы ответили правильно на {} из {}",
            "Қазақ": "{} дурыс {} барлыгы"
        }
    }

    def get_text(self, text, telegram_id, user_s):
        return self.data[text][user_s.get_user_language(telegram_id=telegram_id)]

    def check_text(self, text, message):
        for language, language_text in self.data[text].items():
            if language_text == message:
                return True
        return False
