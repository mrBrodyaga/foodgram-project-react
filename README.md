# Foodgram

https://github.com/mrbrodyaga/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg

### Описание
Продуктовый помощник.
### Технологии
```
Python
Django
DRF
Docker
gunicorn
nginx

```

### Запуск проекта в dev-режиме

- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```sh
pip install -r requirements.txt
```
- Поднять nginx для работы со статикой и db - postgresql - для работы с базой данных
```sh
docker compose up -d db nginx
```
- В папке с файлом [manage.py](manage.py) выполните команды:

```sh
python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

### Адрес сервера

130.193.54.14

### Авторы

mrBrodyaga

ps  я дико извеняюсь за этот говнокод, но завтра уезжаю в командировку.
    пожалуйста проверьте, что есть иначе совсем нифига не успею
    и да нифига не работает.
