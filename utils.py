from aiogram.dispatcher.filters.state import State, StatesGroup


def calc_results(results):
    score = 0
    for result in results:
        if result:
            score += 1
    return [score, len(results)]


class ReferralStates(StatesGroup):
    REFERRAL_STATE_0 = State()
