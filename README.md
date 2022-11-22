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

![изображение](https://user-images.githubusercontent.com/107147438/197279455-e0d8e0a0-f84d-45d7-826c-67ea86e1ab12.png)


Написан в рамках проекта на основе курса "Быстро пишем API на Python с FastAPI" (https://stepik.org/course/119770/)

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


Written as part of a project based on the course "Quickly write API in Python with FastAPI" (https://stepik.org/course/119770/)

***With own implementations of most handlers, error handlers and application template.***

