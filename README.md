# Диплом - Foodgram

![foodgram workflow](https://github.com/abctpu9ihob/yamdb_final/actions/workflows/foodgram_workflow.yml/badge.svg)

http://51.250.81.165/redoc/

### Краткое описание проекта

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Запуск приложения в контейнерах

Разверните проект:

```cd infra/```

```docker-compose up```

Выполните миграции:

```docker-compose exec web python manage.py migrate```

[Опционально] Для быстрого наполнения базы тестовыми данными выполните команду:

```docker-compose exec web python manage.py import_db```

Создайте суперпользователя:

```docker-compose exec web python manage.py createsuperuser```

Собрать всю «статику» проекта:

```docker-compose exec web python manage.py collectstatic --no-input```

***
### Авторы
ABCTPu9IHOB

### License
MIT