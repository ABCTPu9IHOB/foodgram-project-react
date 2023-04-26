# Диплом - Foodgram

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```cd backend/```

Cоздать и активировать виртуальное окружение:

```python3 -m venv venv```

```source venv/bin/activate```

Установить зависимости из файла requirements.txt:

```python3 -m pip install --upgrade pip```

```pip install -r requirements.txt```

Перейти в директорию с manage.py и выполнить миграции:

```python3 manage.py migrate```

[Опционально] Для быстрого наполнения базы тестовыми данными (ингредиентами) выполните команду:

```python3 manage.py import_db```

Запустить проект:

```python3 manage.py runserver```
