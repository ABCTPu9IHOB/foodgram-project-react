# Диплом - Foodgram

![foodgram workflow](https://github.com/abctpu9ihob/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Demo:

http://158.160.41.226/

```bot@yandex.ru - bot12345```

```bob@yandex.ru - bob12345```

http://158.160.41.226/admin (админка)

```admin@yandex.ru - admin```

http://158.160.41.226/api/docs/ (redoc)

### Краткое описание проекта

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Запуск приложения в контейнерах

Разверните проект:

```cd infra/```

```docker-compose up```

Выполните миграции:

```docker-compose exec web python manage.py migrate```

[Опционально] Для быстрого наполнения базы тестовыми данными выполните команду (в Demo уже всё есть):

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
