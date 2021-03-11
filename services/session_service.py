from data.models import Session
from config import Config
import requests


def post_response(session):
    json_session = {
        "topic_name": session.topic_name,
        "owner_id": session.telegram_id,
        "quizzes": session.quiz_ids,
        "results": str(session.results)
    }
    r = requests.post(Config.API_URL+"sessions", json=json_session)
    print(json_session)
    print("session request ", r)


class SessionService:
    sessions = {}

    def create_session(self, telegram_id, topic_name, quiz_ids):
        session = Session(telegram_id=telegram_id, topic_name=topic_name, quiz_ids=quiz_ids, results=[])
        self.sessions[telegram_id] = session

    def post_session(self, telegram_id, results):
        self.sessions[telegram_id].results = results
        post_response(session=self.sessions[telegram_id])