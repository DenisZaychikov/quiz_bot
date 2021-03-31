import os

DIRECTORY_PATH = 'questions'


def get_questions_and_answers():
    questions_and_answers = {}
    files = os.listdir(DIRECTORY_PATH)
    for file in files:
        with open(os.path.join(DIRECTORY_PATH, file), encoding='KOI8-R') as f:
            file_info = f.read().split('\n\n')
            question = ''
            for item in file_info:
                if 'Вопрос' in item:
                    _, question = item.split(':\n', 1)
                if 'Ответ' in item:
                    _, answer = item.split('\n', 1)
                    questions_and_answers[question] = answer

    return questions_and_answers
