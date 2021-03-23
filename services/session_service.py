from data.models import Session
from config import Config
import requests_async as requests

# MARK: Post session to API


async def post_session(session):
    if len(session.results) == 0:
        return
    json_session = {
        "topic_name": Config.DATA_SUBJECT_NAME[session.topic_name],
        "owner_id": [session.telegram_id],
        "quizzes": session.quiz_ids[:len(session.results)],
        "results": session.results
    }
    r = await requests.post(Config.API_URL+Config.SESSION_DB, json=json_session)
    print(json_session)
    print("session request ", r)


class SessionService:
    sessions = {}

    def create_session(self, telegram_id, topic_name, quiz_ids):
        session = Session(telegram_id=telegram_id, topic_name=topic_name, quiz_ids=quiz_ids, results=[])
        self.sessions[telegram_id] = session

    async def post_session(self, telegram_id, results):
        self.sessions[telegram_id].results = results
        await post_session(session=self.sessions[telegram_id])
        self.sessions.pop(telegram_id)

    def have_active_session(self, telegram_id):
        return telegram_id in self.sessions
