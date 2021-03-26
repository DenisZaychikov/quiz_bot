import os
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import logging
from dotenv import load_dotenv
import random
import redis

DIRECTORY_PATH = 'questions'
NEW_QUESTION, ANSWER = range(2)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_short_answer(answer):
    for num, symbol in enumerate(answer):
        if symbol == '.' or symbol == '(':
            short_answer = answer[:num].strip()

            return short_answer


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


def start(bot, update):
    keyboard = [
        ['Новый вопрос', 'Сдаться'],
        ['Мой счет']
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)

    update.message.reply_text(
        text='Привет! Я бот для викторин! Давай поиграем!',
        reply_markup=reply_markup)

    return NEW_QUESTION


def give_up(bot, update):
    answer = get_short_answer(questions_and_answers[r.get(user_chat_id)])
    update.message.reply_text(text=answer)

    handle_new_question_request(bot, update)


def handle_new_question_request(bot, update):
    random_question = random.choice(list(questions_and_answers.keys()))
    # print(questions_and_answers[random_question])
    r.set(user_chat_id, random_question)
    update.message.reply_text(text=random_question)

    return ANSWER


def handle_solution_attempt(bot, update):
    answer = 'Неправильно… Попробуешь ещё раз?'
    if update.message.text == get_short_answer(
            questions_and_answers[r.get(user_chat_id)]):
        answer = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».'
        update.message.reply_text(text=answer)

        return NEW_QUESTION

    update.message.reply_text(text=answer)

    return ANSWER


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(bot, update):
    return ConversationHandler.END


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    user_chat_id = os.getenv('USER_CHAT_ID')
    questions_and_answers = get_questions_and_answers()
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    updater = Updater(token=tg_bot_token)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NEW_QUESTION: [
                MessageHandler(Filters.regex(r'Новый вопрос'),
                               handle_new_question_request),
                MessageHandler(Filters.text, start)
            ],
            ANSWER: [
                MessageHandler(Filters.regex(r'Новый вопрос'),
                               handle_new_question_request),
                MessageHandler(Filters.regex(r'Сдаться'),
                               give_up),
                MessageHandler(Filters.text, handle_solution_attempt),
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()