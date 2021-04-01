# Бот для проведения викторины
Чат-бот с каверзными вопросами и единственным правильным вариантом ответа. Кто победит – того и табуретка смотрителя!
Можно использовать как для телеграм, так и для Вконтакте.

### Пример бота в телеграм - @task4_quiz_bot

![](https://dvmn.org/filer/canonical/1569215494/324/)

### Пример бота во Вконтакте

![](https://dvmn.org/filer/canonical/1569215498/325/)

### Как установить
Для использования бота в телеграм необходимо зарегистрировать бота и получить его токен.
Для использования бота для Вконтакте необходимо зарегистрировать приложение и получить персональный ключ доступа. 
Для сообщества также следует включить сообщения и возможности ботов.
Создайте свой аккаунт в [Redislabs](https://redislabs.com/), 
где вы получите адрес базы данных вида: redis-13965.f18.us-east-4-9.wc1.cloud.redislabs.com,
его порт вида: 16635 и его пароль.

Создайте в корневой папке файл ```.env``` и пропишите в нем переменные следующим образом:  

    ```
    TG_BOT_TOKEN=токен телеграм-бота
    VK_BOT_TOKEN=токен группы вконтакте
    USER_CHAT_ID=ваш chat_id в телеграм
    REDIS_HOST=redis-14588.c243.eu-west-1-3.ec2.cloud.redislabs.com
    RADIS_PORT=14588
    REDIS_PASSWORD=txpKMLjzGkBC97N3i883U7xVdf1K43zx
    ```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Для запуска бота в телеграм:

```python
python tg_quiz_bot.py
```
Для запуска бота во Вконтакте:

```python
python vk_quiz_bot.py
```
