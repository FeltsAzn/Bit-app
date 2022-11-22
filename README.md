# Криптокошелек

***Описание***

Веб кошелек для крипто монет.
- Для визуального отображения и взаимодействия используется телеграм бот.
- Обработчиком запросов от пользователя является приложение fastapi.
- Использующаяся база данных: PostgreSQL

Телеграм бот сделан на основе библиотеки **pyTelegramBotApi//telebot**(для взаимодействия с Телеграмом) и библиотеки **Bit** (для работы с криптовалютой). 

Есть интерфейс для пользователя:
- Проверка баланса
- Создание транзакций
- Просмотр совершённых транзакций

Реализована отдельная панель администратора для отображения:
- Общий баланс всех кошельков
- Отображение списка всех пользователей с перелистыванием по 5 человек (для удобного отображение при большой количестве пользователей)
  - Получение подробной информации по каждому пользователю
  - Возможность удалить пользователя
   
Приложение обработки запросов сделано на основе библиотеки **FastAPI**, так же используютя надстройки jose(JWT-токен сессии) и ponyorm для работы с базой данных.


Доступ к обработчикам приложения происходит за счёт секретного ключа для пользователей (secret_key) и секретного логина и пароля для администратора (oauth2-схема).

______________________________

## Локальное развёртывание

Скопируйте через terminal репозиторий:
```bash
git clone https://github.com/FeltsAzn/Bit_app
```

#### Если вы работаете через редакторы кода `vim`, `nano`, `notepad` и другие:
Установка виртуального окружения, если у вас нет его локально.
```bash
python3 -m pip install --user virtualenv
```

Создайте виртуальное окружение в скопированном репозитории:
```bash
python3 -m venv env
```

Активируйте виртуальное окружение:
```bash
source env/bin/activate
```

Установите файл с зависимостями в виртуальном окружении:
```bash
(venv):~<путь до проекта>$ pip install -r requirements.txt
```

Создайте в папке `tg_bot` файл `tg_bot_config.py` и в папке `fastapi_app` файл `fastapi_config.py`

```bash
touch tg_bot/tg_bot_config.py
touch fastapi_app/fastapi_config.py
```

#### Если вы работаете через IDE:
Создайте файл ***tg_bot_config.py*** в папке проекта ***tg_bot***


Содержание файла `tg_bot_config.py`:
```sh
BOT_TOKEN = <токен бота от BotFather>
ADMIN_ID = (<telegram id админа>, )
ADMIN_PASSWORD = <секретный пароль>
API_URL = "http://127.0.0.1:8000" # пример url
SECRET_HEADER = "e0835cd4f08180f217759dfa692d075e51934a265b9e1f4815b17bf296732e4f" # пример секретного заголовка для связи с ботом
```

Создайте файл ***fastapi_config.py*** в папке проекта ***fastapi_app***

Содержание файла `fastapi_config.py`
```sh
USERNAME = '<telegram id админа>'
PASSWORD = '<пароль>' #HS256
SECRET_KEY = "<секретный ключ>" #HS256
ALGORITHM = "HS256"
SECRET_HEADER = "e0835cd4f08180f217759dfa692d075e51934a265b9e1f4815b17bf296732e4f" # пример секретного заголовка для связи с сервером
```

!!! ВАЖНО
SECRET_HEADER должен быть одинаковый для `tg_bot_config.py` и `fastapi_config.py`

#### Docker контейнер
Вы можете развернуть приложение на сервере или локально в контейнере используя ***dockerfile***:
```bash
docker build . -t <название образа>
```

И запустить собранный образ в контейнере:
```bash
docker run -d <название образа>
```


![изображение](https://user-images.githubusercontent.com/107147438/197279455-e0d8e0a0-f84d-45d7-826c-67ea86e1ab12.png)


Написан в рамках проекта на основе курса "[Быстро пишем API на Python с FastAPI](https://stepik.org/course/119770/)"

***С собственной реализаций большинства обработчиков, обработчиков ошибок и шаблона приложений.***



# Crypto wallet

***Description***

Web wallet for crypto coins.
- Telegram bot is used for visual display and interaction. 
- The handler of requests from the user is the fastapi application. 
- Database used: PostgreSQL.

The Telegram bot is based on the **pyTelegramBotApi//telebot** library (for interacting with Telegram) and the **Bit** library (for working with cryptocurrency).

There is a user interface:
- Balance check
- Create transactions
- View completed transactions

A separate admin panel has been implemented to display:
- Total balance of all wallets
- Displaying a list of all users with scrolling by 5 people (for convenient display with a large number of users)
  - Get detailed information for each user
  - Ability to delete a user
   
The request processing application is based on the **FastAPI** library, it also uses the jose (JWT session token) and ponyorm add-ons to work with the database.


Access to the application handlers occurs through a secret key for users (secret_key) and a secret login and password for the administrator (oauth2 scheme).

______________________________

## Local deployment

Copy via terminal repository:
```bash
git clone https://github.com/FeltsAzn/Bit_app
```

#### If you are working with code editors `vim`, `nano`, `notepad` and others:
Installing a virtual environment if you don't have one locally.
```bash
python3 -m pip install --user virtualenv
```

Create a virtual environment in the copied repository:
```bash
python3 -m venv env
```

Activate the virtual environment:
```bash
source env/bin/activate
```

Install the dependency file in the virtual environment:
```bash
(venv):~<project path>$ pip install -r requirements.txt
```

Create `tg_bot_config.py` file in `tg_bot` folder and `fastapi_config.py` file in `fastapi_app` folder

```bash
touch tg_bot/tg_bot_config.py
touch fastapi_app/fastapi_config.py
```

#### If you are using the IDE:
Create file ***tg_bot_config.py*** in project folder ***tg_bot***


Contents of `tg_bot_config.py` file:
```sh
BOT_TOKEN = <bot token from BotFather>
ADMIN_ID = (<telegram admin id>, )
ADMIN_PASSWORD = <secret password>
API_URL = "http://127.0.0.1:8000" # example url
SECRET_HEADER = "e0835cd4f08180f217759dfa692d075e51934a265b9e1f4815b17bf296732e4f" # an example of a secret header for communicating with a bot
```

Create file ***fastapi_config.py*** in project folder ***fastapi_app***

Contents of `fastapi_config.py` file
```sh
USERNAME = '<telegram admin id>'
PASSWORD = '<password>' #HS256
SECRET_KEY = "<secret key>" #HS256
ALGORITHM="HS256"
SECRET_HEADER = "e0835cd4f08180f217759dfa692d075e51934a265b9e1f4815b17bf296732e4f" # an example of a secret header for communicating with the server
```

!!! IMPORTANT
SECRET_HEADER must be the same for `tg_bot_config.py` and `fastapi_config.py`

#### Docker container
You can deploy the application on a server or locally in a container using ***dockerfile***:
```bash
docker build . -t <image name>
```

And run the built image in a container:
```bash
docker run -d <image name>
```

Written as part of a project based on the course "[Quickly write API in Python with FastAPI](https://stepik.org/course/119770/)"

***With own implementations of most handlers, error handlers and application template.***

