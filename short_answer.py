def get_short_answer(answer):
    for num, symbol in enumerate(answer):
        if symbol == '.' or symbol == '(':
            short_answer = answer[:num].strip()

            return short_answer
