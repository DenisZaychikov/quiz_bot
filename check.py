def get_short_answer(answer):
    for num, symbol in enumerate(answer):
        if symbol == '.' or symbol == '(':
            short_answer = answer[:num]

            return short_answer


a = 'Гончарова. (Это список серьезных увлечений Пушкина.)'

print(get_short_answer(a))