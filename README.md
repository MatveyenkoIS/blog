# Блог с Clean Architecture
- Post, Comment, User
- 3 слоя архитектуры
- SQLite база
- 2-3 паттерна (Repository, Factory)
- Postman коллекция

### Структура проекта

```
blog/
├── application/
│   └── use_cases.py
├── domain/
│   ├── entities.py
│   ├── factories.py
│   └── repositories.py
├── infrastructure/
│   ├── database.py
│   ├── factories.py
│   └── repositories.py
├── interfaces/
│   └── web/
│       ├── app.py
│       └── controllers.py
├── tests/
│   └── test_blog.py
├── requirements.txt
├── run.py
└── postman_collection.json
```