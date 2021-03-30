import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from dotenv import load_dotenv
import os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import redis


def echo(event, vk_api):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.NEGATIVE)

    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        keyboard=keyboard.get_keyboard(),
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_bot_token = os.getenv('VK_BOT_TOKEN')
    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
