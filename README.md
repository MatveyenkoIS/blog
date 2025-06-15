# Блог с Clean Architecture

## Техническое задание

- Post, Comment, User
- 3 слоя архитектуры
- SQLite база
- 2-3 паттерна (Repository, Factory)
- Postman коллекция

## Структура проекта

```
blog/
├── application/
|   ├── __init__.py
│   └── use_cases.py
├── domain/
|   ├── __init__.py
│   ├── entities.py
│   ├── factories.py
│   └── repositories.py
├── infrastructure/
|   ├── __init__.py
│   ├── database.py
│   ├── factories.py
│   └── repositories.py
├── interfaces/
|   ├── __init__.py
│   └── web/
|       ├── __init__.py
│       ├── app.py
│       └── controllers.py
├── tests/
|   ├── __init__.py
│   └── test_blog.py
├── postman_collection.json
├── requirements.txt
├── run.py
└── setup.py
```