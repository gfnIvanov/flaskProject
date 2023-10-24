# Учебный проект на базе фреймворка Flask

## Общее описание 
# Тест

Веб-приложение, использующее базовые возможности фреймворка flask для реализации функциональности тематического блога со следующим набором возможностей:

- Регистрация и авторизация
- Ограничение доступа к контенту для неавторизованных пользователей
- Добавление и редактирование статей
- Перевод страницы при помощи внешнего сервиса
- Обучение модели на наборе данных [House Prices](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data)
- Получение предсказаний модели по случайному набору данных в структуре House Prices

## Описание отдельных функциональных блоков

### Регистрация и авторизация

Реализованы в модальных окнах с валидацией вводимых пользователем данных. При регистрации данные сохраняются в стандартный раздел Users (предоставляется фреймворком) и производится автоматический вход. При успешной авторизации данные пользователя сохраняютя в сессии и используются для контроля доступа к разделам приложения.

### Перевод страницы

Все статичные блоки (элементы управления хедера и футера) переводятся простым сопоставлением в js-функциях. Для перевода изменяемых текстовых блоков используется сервис [Yandex Translate](https://cloud.yandex.ru/services/translate), который для обхода ограничений CORS использует serverless-функцию в сервисе [Yandex Cloud Functions](https://cloud.yandex.ru/services/functions).

### Сборка и запуск

Для унификации CLI-команд в ходе разработки используется Makefile. Сборка осуществляется при помощи docker-compose (создание контейнера с приложением и контейнера с базой данных MySQL).

### Machine Learning

Демонстрационная функциональность. Модель обучается с помощью алгоритма регрессии [xgboost.XGBRegression](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBRegressor). Интерфейс позволяет загрузить csv-файл с подготовленными данными для обучения. По завершении обучения пользователь переводится на страницу использования модели, где может сравнить реальный результат по случайному набору данных и результат, предсказанный моделью.

## Технологии

![Flask](https://img.shields.io/badge/flask-%23092E20.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
