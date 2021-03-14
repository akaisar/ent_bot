def calc_results(results):
    score = 0
    for result in results:
        if result:
            score += 1
    return [score, len(results)]