from aiogram.dispatcher.filters.state import State, StatesGroup


def calc_results(results):
    score = 0
    for result in results:
        if result:
            score += 1
    return [score, len(results)]


class ReferralStates(StatesGroup):
    REFERRAL_STATE_0 = State()


class UserNameStates(StatesGroup):
    USER_NAME_STATE_0 = State()


class TeacherStatStates(StatesGroup):
    TEACHER_STAT_STATE_0 = State()


class SynopsesStates(StatesGroup):
    SYNOPSES_STATE_0 = State()


class SubjectsStates(StatesGroup):
    SUBJECTS_STATE_0 = State()
    SUBJECTS_STATE_1 = State()


class SessionStates(StatesGroup):
    SESSION_STATE_0 = State()