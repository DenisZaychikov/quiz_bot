import os
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import logging
from dotenv import load_dotenv
import random
import redis
from questions import get_questions_and_answers
from short_answer import get_short_answer

logger = logging.getLogger(__name__)

NEW_QUESTION, ANSWER = range(2)


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
    answer = questions_and_answers[r.get(user_chat_id)]
    short_answer = get_short_answer(answer)
    update.message.reply_text(text=short_answer)

    handle_new_question_request(bot, update)


def handle_new_question_request(bot, update):
    random_question = random.choice(list(questions_and_answers.keys()))
    r.set(user_chat_id, random_question)
    update.message.reply_text(text=random_question)

    return ANSWER


def handle_solution_attempt(bot, update):
    answer = 'Неправильно… Попробуешь ещё раз?'
    answer_from_data = questions_and_answers[r.get(user_chat_id)]
    if update.message.text == get_short_answer(answer_from_data):
        answer = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».'
        update.message.reply_text(text=answer)

        return NEW_QUESTION

    update.message.reply_text(text=answer)

    return ANSWER


def error_handler(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(bot, update):
    return ConversationHandler.END


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    user_chat_id = os.getenv('USER_CHAT_ID')
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('RADIS_PORT')
    redis_password = os.getenv('REDIS_PASSWORD')
    questions_and_answers = get_questions_and_answers()
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password,
                    db=0, decode_responses=True)
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
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
