import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from dotenv import load_dotenv
import os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import redis
from questions import get_questions_and_answers
from short_answer import get_short_answer


def start(event, vk_api, message, keyboard):
    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


def handle_new_question_request(event, keyboard):
    random_question = random.choice(list(questions_and_answers.keys()))
    r.set(event.user_id, random_question)

    vk_api.messages.send(
        user_id=event.user_id,
        message=random_question,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


def give_up(event, vk_api):
    short_answer = get_short_answer(
        questions_and_answers[r.get(event.user_id)])

    vk_api.messages.send(
        user_id=event.user_id,
        message=short_answer,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


def handle_solution_attempt(event, vk_api):
    answer = 'Неправильно… Попробуешь ещё раз?'
    if event.text == get_short_answer(
            questions_and_answers[r.get(event.user_id)]):
        answer = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».'

    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_bot_token = os.getenv('VK_BOT_TOKEN')
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('RADIS_PORT')
    redis_password = os.getenv('REDIS_PASSWORD')
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    questions_and_answers = get_questions_and_answers()
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password,
                    db=0, decode_responses=True)
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.NEGATIVE)
    start_command = False
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                handle_new_question_request(event, keyboard)
            elif event.text == 'Сдаться':
                give_up(event, vk_api)
                handle_new_question_request(event, keyboard)
            elif start_command:
                handle_solution_attempt(event, vk_api)
            else:
                start_command = True
                message = 'Привет! Я бот для викторин! Давай поиграем!'
                start(event, vk_api, message, keyboard)
