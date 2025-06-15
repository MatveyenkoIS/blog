# Блог с Clean Architecture

## Техническое задание (на оценку 4)

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

## Инструкция по запуску проекта

Рекомендуется использовать терминал Git Bash

1. Создайте виртуальное окружение

```
python -m venv venv
```

2. Активируйте виртуальное окружение

```
source venv/Scripts/activate
```

3. Установите менеджер пакетов pip

```
pip install -U pip
```

4. Установите зависимости из requirements.txt

```
pip install -r requirements.txt
```

5. Если нужно, проведите проверку установленных зависимостей

```
pip list
```

6. Запустите проект командой

```
python run.py
```

## Документация Swagger

Для проекта была создана Swagger-документация с использованием расширения Flasgger. Ознакомиться с ней можно по ссылке ниже (*предварительно запустите проект с помощью* ```python run.py```).

Ссылка: [http://localhost:5000/apidocs]

![](https://github.com/MatveyenkoIS/blog/raw/main/images/swagger.png)

## Запуск тестов

1. Для запуска тестов Pytest введите в терминал Git Bash следующую команду:

```
pytest tests/
```

2. Для работы с коллекцией Postman необходимо установить Postman Desktop с [https://www.postman.com/downloads/](официального сайта).

3. Запустите проект, если до этого он у вас был отключён, командой

```
python run.py
```

4. Запустите программу и перейдите на вкладку Internal Workspace в левом верхнем углу интерфейса

![](https://github.com/MatveyenkoIS/blog/raw/main/images/workspace.png)

5. В открывшемся меню нажмите на кнопку Import

![](https://github.com/MatveyenkoIS/blog/raw/main/images/import.png)

6. В открывшемся попапе нажмите на files

![](https://github.com/MatveyenkoIS/blog/raw/main/images/popup.png)

7. Найдите в корне проекта файл postman_collection.json, кликните на него левой кнопкой мыши и нажмите Открыть

![](https://github.com/MatveyenkoIS/blog/raw/main/images/collection.png)

8. Вернитесь в интерфейс Postman. Во вкладке Collections наведитесь курсором на Blog API и нажмите на символ трёх точек. В выпадающем меню выберите пункт Run

![](https://github.com/MatveyenkoIS/blog/raw/main/images/run.png)

9. В новом меню нажмите на кнопку Run Blog API

![](https://github.com/MatveyenkoIS/blog/raw/main/images/blogAPI.png)

10. Наслаждайтесь результатом 🤩

![](https://github.com/MatveyenkoIS/blog/raw/main/images/result.png)