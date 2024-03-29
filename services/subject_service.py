import requests_async as requests
import json
from localization.localization import Data
from config import Config
import logging
from data.models import Subject, Subtopic


def subject_json_to_obj(json_obj):
    return Subject(
        topic_name=Config.SUBJECT_NAME_DATA[json_obj["subject_name"]],
        subtopics=json_obj["subtopics"]
    )


def subtopic_json_to_obj(json_obj):
    return Subtopic(
        topic_id=json_obj["id"],
        topic_name=json_obj["subtopic"],
        text=json_obj["lecture_notes"]
    )


async def get_subjects_from_api():
    r = await requests.get(Config.API_URL+Config.SUBJECTS_DB)
    data = json.loads(r.text)
    subjects = {}
    for json_subject in data:
        subject = subject_json_to_obj(json_subject)
        subjects[Config.SUBJECT_NAME_DATA[json_subject["subject_name"]]] = subject
    subtopics = {}
    for topic_name, subject in subjects.items():
        for subtopic_id in subject.subtopics:
            r = await requests.get(Config.API_URL+Config.SUBTOPIC_DB+'/'+str(subtopic_id))
            json_subtopic = json.loads(r.text)[0]
            subtopic = subtopic_json_to_obj(json_subtopic)
            subtopics[json_subtopic["subtopic"]] = subtopic
            subtopics[json_subtopic["id"]] = subtopic
    return subjects, subtopics


class SubjectService:
    subjects = {}
    subtopics = {}

    async def load_subjects(self):
        logging.info("start load synopses")
        self.subjects, self.subtopics = await get_subjects_from_api()
        logging.info("finish load synopses")

    def get_subject_topics(self, topic_name):
        topic_names = []
        for subtopic in self.subjects[topic_name].subtopics:
            topic_names.append(self.subtopics[subtopic].topic_name[0])
        return topic_names

    def get_subtopic_text(self, topic_name):
        return self.subtopics[topic_name].text

    def is_subtopic_name(self, topic_name):
        return topic_name in self.subtopics
