import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from dotenv import load_dotenv
import random
import redis
import pdb

DIRECTORY_PATH = 'questions'

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

    update.message.reply_text(text='Привет! Я бот для викторин!',
                              reply_markup=reply_markup)


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    answer = 'Неправильно… Попробуешь ещё раз?'
    if update.message.text == 'Новый вопрос':
        random_question = random.choice(list(questions_and_answers.keys()))
        r.set(user_chat_id, random_question)
        answer = random_question
        print(questions_and_answers[random_question])
    if update.message.text == get_short_answer(
            questions_and_answers[r.get(user_chat_id)]):
        answer = 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».'

    update.message.reply_text(text=answer)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    user_chat_id = os.getenv('USER_CHAT_ID')
    questions_and_answers = get_questions_and_answers()
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    updater = Updater(token=tg_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()