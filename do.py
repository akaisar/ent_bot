def set_hook():
    import asyncio
    from config import Config
    from aiogram import Bot
    bot = Bot(token=Config.TOKEN)

    async def hook_set():
        if not Config.HEROKU_APP_NAME:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(Config.WEBHOOK_URL)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    bot.close()


def start():
    from setup import main
    main()
