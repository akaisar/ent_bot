import os


class Config:
    API_URL = 'http://aldie1741.pythonanywhere.com/'
    TOKEN = os.getenv('API_BOT_TOKEN')
    ADMIN_IDS = [int(i) for i in os.getenv('OWNER_ID').split()]
