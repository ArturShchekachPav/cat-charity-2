# QRKot — благотворительный фонд поддержки котиков

REST API для фонда **QRKot**. Позволяет создавать целевые проекты, принимать пожертвования и автоматически распределять поступившие средства между открытыми проектами.

## Как это работает

- Создаётся новый проект → свободные пожертвования сразу идут в него.
- Поступает новое пожертвование → оно автоматически распределяется между открытыми проектами.

Инвестирование запускается при каждом создании проекта/пожертвования и выполняется в одной транзакции с ним.

Присутствует авторизация и защита ручек. Есть 3 категории пользователей: неавторизованные, авторизованные и суперпользователи

## Стек

- Python, FastAPI, FastAPI Users, Uvicorn
- SQLAlchemy, Pydantic
- SQLite

## Запуск

```bash
git clone <URL>
cd cat-charity-1
python -m venv venv && source venv/Scripts/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

По умолчанию используется `sqlite+aiosqlite:///./fastapi.db`.

## Тесты и линтер

```bash
pytest
flake8 app/
```

## Автор

**Артур Щекач**
- GitHub: [@ArturShchekachPav](https://github.com/ArturShchekachPav)
- Email: ashhekach@gmail.com

## Лицензия

Проект создан в учебных целях