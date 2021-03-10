from data.models import Session
from config import Config
import requests


def post_response(session):
    requests.post(Config.API_URL+"", json=session.__dict__)


class SessionService:
    sessions = {}

    def create_session(self, telegram_id, topic_name, quiz_ids):
        session = Session(telegram_id=telegram_id, topic_name=topic_name, quiz_ids=quiz_ids, results=[])
        self.sessions[telegram_id] = session

    def post_session(self, telegram_id, results):
        self.sessions[telegram_id].results = results
        post_response(session=self.sessions[telegram_id])