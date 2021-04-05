# Бот для проведения викторины
чат-бот с каверзными вопросами и единственным правильным вариантом ответа. Кто победит – того и табуретка смотрителя!
Можно использовать как для телеграм, так и для Вконтакте.

Пример бота в телеграм - @task4_quiz_bot
![](https://dvmn.org/filer/canonical/1569215494/324/)

Пример бота во Вконтакте
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
    DIRECTORY_PATH=путь к папке с файлами, содержащие вопросы и ответы
```    
Чтобы добавить новые вопросы для бота, необходимо создать txt-файл с кодировкой `KOI8-R` 
Пример данного файла:
```txt
Вопрос 1:
С одним советским туристом в Марселе произошел такой случай. Спустившись
из своего номера на первый этаж, он вспомнил, что забыл закрутить кран в
ванной. Когда он поднялся, вода уже затопила комнату. Он вызвал
горничную, та попросила его обождать внизу. В страхе он ожидал расплаты
за свою оплошность. Но администрация его не ругала, а, напротив,
извинилась сама перед ним. За что?

Ответ:
За то, что не объяснила ему правила пользования кранами.


Вопрос:
Средневековый обычай: рыцаря, совершившего поступок, порочащий честь,
заставляли пробежать некоторую дистанцию, положив ему на спину седло,
мешок с камнями или... Кого?

Ответ:
Собаку. Отсюда, по одной из версий, происходит выражение "навешать
собак".
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