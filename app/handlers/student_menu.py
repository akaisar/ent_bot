

async def start(message: types.Message):
    telegram_id = message.from_user.id
    is_new_user = await user_s.post_user(telegram_id=telegram_id)
    language = user_s.get_language(telegram_id=telegram_id)
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text=local.data[Data.MAIN_MENU_BUTTON][language]))
    if is_new_user:
        for language in local.languages:
            if local.languages[-1] != language:
                await message.answer(text=local.data[Data.NEW_USERS_WELCOME_MESSAGE][language])
            else:
                await message.answer(text=local.data[Data.NEW_USERS_WELCOME_MESSAGE][language],
                                     reply_markup=poll_keyboard)
    else:
        await message.answer(text=local.data[Data.WELCOME_MESSAGE][language], reply_markup=poll_keyboard)
